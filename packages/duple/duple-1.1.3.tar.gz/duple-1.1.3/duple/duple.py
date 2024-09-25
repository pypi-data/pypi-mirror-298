import click
from pathlib import Path
import os
import hashlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from itertools import repeat
from humanize import naturalsize
import json
from collections import Counter
from send2trash import send2trash
from time import perf_counter
from datetime import datetime as dt
from datetime import timezone
from random import choice
from duple.__version__ import __version__

"""
To Do:
1. Add filtering capability for files (only pictures or files after a certain date)

"""


def get_available_hashes() -> list:
    hashes = list(hashlib.algorithms_available)
    hashes.remove("shake_128")
    hashes.remove("shake_256")
    hashes.sort()
    return hashes


def get_hash(path: str, hash: str) -> str | str:
    with open(path, "rb") as f:
        digest = hashlib.file_digest(f, hash)
    return digest.hexdigest(), path


def timed_get_hash(hash: str, path: str) -> float:
    start = perf_counter()
    get_hash(path, hash)
    finish = perf_counter()
    return hash, finish - start


def dict_from_stat(stats: os.stat_result) -> dict:
    temp = (
        repr(stats)
        .replace("os.stat_result(", "")
        .replace(")", "")
        .replace(" ", "")
        .split(",")
    )
    result = dict()
    for item in temp:
        temp_item = item.split("=")
        result[temp_item[0]] = int(temp_item[1])
    return result


def dump_dict_to_json(input: dict, filename: str, indent: int = 4):
    with open(filename, "w") as f:
        json.dump(input, f, indent=indent)


def traverse_files(path: str) -> dict | list:
    # cycle through all files collecting information
    result = dict()
    #  key = path, value = dictionary
    #     value dictionary:
    #         os.stat_result
    #         depth
    #         type

    for root, dirs, files in tqdm(
        os.walk(path, followlinks=False), desc="Preprocessing File Tree"
    ):
        for file in files:
            temp = str(Path(f"{root}/{file}").absolute())
            tempPath = Path(temp)
            if tempPath.exists():
                result[temp] = dict_from_stat(tempPath.stat())
                result[temp]["type"] = "ignored"
                result[temp]["depth"] = len(tempPath.parents)

    sizes = dict()
    for key, value in result.items():
        if value["st_size"] not in sizes.keys():
            sizes[value["st_size"]] = list()
        sizes[value["st_size"]].append(key)

    potential_duplicates = list()
    for key, value in sizes.items():
        if len(value) > 1:
            for file in value:
                result[file]["type"] = "potential_duplicate"
                potential_duplicates.append(file)

    return result, potential_duplicates


def annotate_duplicates(
    hashes: list,
    all_files: dict,
    depth_lowest: bool,
    depth_highest: bool,
    shortest_name: bool,
    longest_name: bool,
    created_oldest: bool,
    created_newest: bool,
    modified_oldest: bool,
    modified_newest: bool,
) -> dict | dict:

    # define test functions
    def path_depth(path: str) -> int:
        return all_files[path]["depth"], path
        return len(Path(path).parents)

    def name_length(path: str) -> int:
        return len(Path(path).name), path

    def created_date(path: str) -> int:
        return all_files[path]["st_birthtime"], path
        return Path(path).stat().st_birthtime

    def modified_date(path: str) -> int:
        return all_files[path]["st_mtime"], path
        return Path(path).stat().st_mtime

    # select the test function based on flag
    options = [
        (depth_lowest, path_depth, 1),
        (depth_highest, path_depth, -1),
        (shortest_name, name_length, 1),
        (longest_name, name_length, -1),
        (created_oldest, created_date, 1),
        (created_newest, created_date, -1),
        (modified_oldest, modified_date, 1),
        (modified_newest, modified_date, -1),
    ]

    for flag, function, option in options:
        if flag:
            test_fun = function
            negate = option

    # group hashes
    grouped_hashes = dict()
    for key, value in hashes:
        if key not in grouped_hashes.keys():
            grouped_hashes[key] = list()
        grouped_hashes[key].append(value)

    dupes = dict()
    for hash, file_paths in grouped_hashes.items():
        for file_path in file_paths:
            all_files[file_path]["hash"] = hash
            if hash not in dupes.keys():
                dupes[hash] = list()
            dupes[hash].append(file_path)

    dupes = {key: value for key, value in dupes.items() if len(value) > 1}

    for value in dupes.values():
        seed, result = test_fun(value[0])
        for file_path in value:
            if file_path in all_files.keys():
                all_files[file_path]["type"] = "duplicate"
                all_files[file_path]["twins"] = len(value) - 1

            if negate * seed > negate * test_fun(file_path)[0]:
                seed, result = test_fun(file_path)

        all_files[result]["type"] = "original"

    for key, value in all_files.items():
        if value["type"] == "potential_duplicate":
            value["type"] = "original"

    return all_files, dupes


def calculate_statistics(all_files: dict) -> dict:
    result = dict()
    result["total files"] = 0
    result["ignored files"] = 0
    result["duplicates"] = 0
    result["duplicate groups"] = 0
    result["total size - duplicates"] = 0
    result["total size - all files"] = 0

    for key, value in all_files.items():

        if value["type"] == "ignored":
            result["ignored files"] += 1

        if value["type"] == "duplicate":
            result["total size - duplicates"] += value["st_size"]
            result["duplicates"] += 1

        if value["type"] == "original":
            result["duplicate groups"] += 1

        result["total size - all files"] += value["st_size"]
        result["total files"] += 1

    result["total size - duplicates"] = naturalsize(result["total size - duplicates"])
    result["total size - all files"] = naturalsize(result["total size - all files"])
    return result


def remove_empty_directories() -> None:

    for root, folders, files in tqdm(
        os.walk(os.getcwd()), desc="Removing .DS_Store files from empty directories"
    ):
        if f".DS_Store" in files and len(files) == 1:
            path = str(Path(root).joinpath(".DS_Store").absolute())
            send2trash(path)

    dirs = list()
    for root, folders, files in os.walk(os.getcwd()):
        if not files and not folders:
            dirs.append(root)

    dirs = sorted(dirs, key=lambda x: -1 * len(Path(x).parents))

    if len(dirs) == 0:
        return

    for dir in tqdm(dirs, desc="Removing empty directories"):
        send2trash(dir)


def get_delete_paths() -> dict:
    if not duple_outputs_exist():
        return

    with open("duple.delete", "r") as f:
        items = f.read().splitlines()

    results = dict()
    flag = False
    for item in items:
        if item == "Duplicate Results:":
            flag = True

        if flag and "----" in item:
            break

        if flag and item.split("|")[0].strip() in ["duplicate", "original"]:
            item_split = item.split("|")
            action = item_split[0].strip()
            size = item_split[1].strip()
            path = item_split[2][1:].strip()
            results[path] = {"type": action, "size": size, "path": path}

    return results


def duple_outputs_exist() -> bool:
    if not Path("duple.delete").exists() or not Path("duple.json").exists():
        click.secho(
            "duple.delete and/or duple.json do no exists - run duple scan to create these files"
        )
        return False
    return True


def create_output(all_files: dict, dupes: dict, summary_statistics: dict) -> None:

    max_len_key = max([len(k) for k in summary_statistics.keys()])
    max_len_val = max([len(str(v)) for v in summary_statistics.values()])
    max_len_type = max([len(v["type"]) for k, v in all_files.items()]) + 2
    max_len_size = (
        max([len(naturalsize(v["st_size"])) for k, v in all_files.items()]) + 2
    )
    section_divider = f"\n{''.rjust(max_len_key + max_len_val + 10,'-')}\n"

    output_json = Path() / 'duple.json'
    output_delete = Path() / 'duple.delete'

    for key, value in summary_statistics.items():
        click.secho(
            f'{key.ljust(max_len_key + max_len_val - len(str(value)) + 10, ".")}{click.style(str(value), fg = "green")}'
        )

    click.secho()
    click.secho(
        "Open the `output summary results` file listed above with a text editor for review",
        fg="yellow",
    )
    click.secho("Once review and changes are complete, run `duple rm`", fg="yellow")

    dump_dict_to_json(all_files, output_json.absolute())

    with open("duple.delete", "w", encoding="utf-8") as f:
        f.write(
            f"Duple Report Generated on {dt.now(timezone.utc).astimezone().isoformat()}, commanded by user: {os.getlogin()}"
        )
        f.write(section_divider)
        f.write("Summary Statistics:\n")
        for key, value in summary_statistics.items():
            f.write(
                f'{key.ljust(max_len_key + max_len_val - len(str(value)) + 10,".")}{str(value)}\n'
            )

        f.write(section_divider)
        f.write("Outputs:\n")
        f.write(f"{str(output_json.absolute())}\n")
        f.write(f"{str(output_delete.absolute())}\n")

        f.write(section_divider)
        f.write("Instructions to User:\n")
        f.write(
            "The sections below describe what action duple will take when 'duple rm' is commanded."
            " The first column is the flag that tells duple what to do:\n"
            "\toriginal   : means duple will take no action for this file, listed only as a reference to the user\n"
            "\tdelete     : means duple will send this file to the trash can or recycling bin, if able\n"
        )

        f.write(section_divider)
        f.write("Duplicate Results:\n")
        if len(dupes.keys()) == 0:
            f.write("No duplicates found.\n")

        for value in dupes.values():
            for file in value:
                if all_files[file]["type"] in ["duplicate", "original"]:
                    flag = str(all_files[file]["type"]).ljust(max_len_type)
                    size = naturalsize(all_files[file]["st_size"]).rjust(max_len_size)
                    f.write(f"{flag}|{size} | {file}\n")
            f.write("\n")

        f.write(section_divider)
        f.write("All Files in Scan:\n")
        for file, stats in all_files.items():
            flag = str(stats["type"]).ljust(max_len_type)
            size = naturalsize(stats["st_size"]).rjust(max_len_size)
            f.write(f"{flag}|{size} | {file}\n")


def get_version() -> str:
    # pyproject = Path(__file__).parent.joinpath('pyproject.toml').absolute()
    # print(pyproject)
    # with open(pyproject, "rb") as f:
    #     data = tomllib.load(f)

    # return data['tool']['poetry']['version']
    return __version__


@click.group()
def cli() -> None:
    pass


@cli.command()
def version() -> str:
    """display the current version of duple"""
    click.secho(f"duple version: {get_version()}")


@cli.command()
@click.argument("path", type=click.STRING)
@click.argument("hash", type=click.STRING)
@click.option(
    "--depth_lowest",
    "-d",
    is_flag=True,
    help="keep the file with the lowest pathway depth",
)
@click.option(
    "--depth_highest",
    "-D",
    is_flag=True,
    help="keep the file with the highest pathway depth",
)
@click.option(
    "--shortest_name", "-s", is_flag=True, help="keep the file with the shortest name"
)
@click.option(
    "--longest_name", "-S", is_flag=True, help="keep the file with the longest name"
)
@click.option(
    "--created_oldest",
    "-c",
    is_flag=True,
    help="keep the file with the oldest creation date",
)
@click.option(
    "--created_newest",
    "-C",
    is_flag=True,
    help="keep the file with the newest creation date",
)
@click.option(
    "--modified_oldest",
    "-m",
    is_flag=True,
    help="keep the file with the oldest modification date",
)
@click.option(
    "--modified_newest",
    "-M",
    is_flag=True,
    help="keep the file with the newest modification date",
)
@click.option(
    "--number_of_cpus",
    "-ncpu",
    type=click.INT,
    help="Maximum number of workers (cpu cores) to use for the scan",
    default=0,
)
@click.option(
    "--chunksize",
    "-ch",
    type=click.INT,
    help="chunksize to give to workers, minimum of 2",
    default=2,
)
def scan(
    path: str,
    hash: str,
    depth_lowest: bool,
    depth_highest: bool,
    shortest_name: bool,
    longest_name: bool,
    created_oldest: bool,
    created_newest: bool,
    modified_oldest: bool,
    modified_newest: bool,
    number_of_cpus: int = 0,
    chunksize: int = 2,
) -> None:
    """
    Scan recursively computes a hash of each file and puts the hash into
    a dictionary.  The keys are the hashes of the files, and the values
    are the file paths and metadata.  If an entry has more than 1 file
    associated, they are duplicates.  The original is determined by the
    flags or options (ex: -d).  The duplicates are added to a file called
    duple.delete.
    """

    perf_start_overall = perf_counter()

    # input validation
    hashes = get_available_hashes()
    if hash not in hashes:
        click.secho(f"Hash must be one of the following: {hashes}")
        return

    if number_of_cpus > os.cpu_count():
        click.secho(
            f"Too many cpus (number_of_cpus too high), only using {os.cpu_count()} cpus"
        )
        number_of_cpus = os.cpu_count()

    if number_of_cpus == 0:
        number_of_cpus = int(int(os.cpu_count() * 2 / 3) + 1)

    if chunksize < 2:
        click.secho(f"chunksize too low, setting to default of 2")
        chunksize = 2

    flags = [
        depth_lowest,
        depth_highest,
        shortest_name,
        longest_name,
        created_oldest,
        created_newest,
        modified_oldest,
        modified_newest,
    ]

    c = Counter(flags)
    if c[True] > 1:
        click.secho("Only one flag can be chosen at a time.")
        return
    if c[True] == 0:
        click.secho(
            "Must select at least one flag to determine handling of duplicates, ex: -d"
        )
        return

    perf_start_file_traversal = perf_counter()
    all_files, potential_duplicates = traverse_files(path)
    perf_finish_file_traversal = perf_counter()

    perf_start_hash = perf_counter()
    hashes = process_map(
        get_hash,
        potential_duplicates,
        repeat(hash),
        max_workers=number_of_cpus,
        chunksize=2,
        desc="Hashing Files...",
    )
    perf_finish_hash = perf_counter()

    perf_start_report_duplicates = perf_counter()
    all_files, dupes = annotate_duplicates(hashes, all_files, *flags)
    perf_finish_report_duplicates = perf_counter()

    perf_start_statistics = perf_counter()
    summary_statistics = calculate_statistics(all_files)
    perf_finish_statistics = perf_counter()

    perf_finish_overall = perf_counter()

    summary_statistics["hash_type"] = hash
    summary_statistics["file system traveral time (seconds)"] = round(
        perf_finish_file_traversal - perf_start_file_traversal, 4
    )
    summary_statistics["hashing time (seconds)"] = round(
        perf_finish_hash - perf_start_hash, 4
    )
    summary_statistics["annotating duplicates (seconds)"] = round(
        perf_finish_report_duplicates - perf_start_report_duplicates, 4
    )
    summary_statistics["calculating statistics time (seconds)"] = round(
        perf_finish_statistics - perf_start_statistics, 4
    )
    summary_statistics["total time (seconds)"] = round(
        perf_finish_overall - perf_start_overall, 4
    )
    summary_statistics["version"] = __version__
    summary_statistics["wrote summary results"] = f"{os.getcwd()}/duple.delete"
    summary_statistics["wrote raw results"] = f"{os.getcwd()}/duple.json"

    create_output(all_files, dupes, summary_statistics)


@cli.command()
@click.option(
    "--verbose", "-v", is_flag=True, help="Use this flag to enter verbose mode"
)
@click.option(
    "--dry_run",
    "-dr",
    is_flag=True,
    help="Perform dry run, do everything except for deleting the files",
)
@click.option(
    "--leave_empty_dirs",
    "-led",
    is_flag=True,
    help="Do not delete empty directories/folders",
)
def rm(verbose: bool, dry_run: bool, leave_empty_dirs: bool) -> None:
    """
    rm sends all 'duplicate' files specified in duple.delete to the trash folder
    """

    message_margin = 16

    if not duple_outputs_exist():
        return

    files = get_delete_paths()

    delete_style = ""
    keep_style = ""

    if verbose:
        delete_style = click.style("deleted".ljust(message_margin), fg="yellow")
        keep_style = click.style("kept".ljust(message_margin), fg="green")

    if dry_run:
        delete_style = click.style("will delete".ljust(message_margin), fg="yellow")
        keep_style = click.style("will keep".ljust(message_margin), fg="green")
        verbose = True

    if not verbose:
        for file, data in tqdm(files.items()):
            if data["type"] == "duplicate" and Path(file).exists():
                send2trash(file)

    if verbose:
        for i, (file, data) in enumerate(files.items()):
            completion_style = click.style(
                f"[{(i / len(files.items()) * 100) : 6.1f}%]", fg="cyan"
            )

            if not dry_run and Path(file).exists() and data["type"] == "duplicate":
                send2trash(file)

            if dry_run or verbose:
                if data["type"] == "original":
                    click.secho(
                        f'{completion_style} {keep_style} {data["size"]} --> {file}'
                    )
                if data["type"] == "duplicate":
                    click.secho(
                        f'{completion_style} {delete_style} {data["size"]} --> {file}'
                    )

    if not dry_run and not leave_empty_dirs:
        remove_empty_directories()


@cli.command()
@click.argument("path", type=str)
def hash_stats(path: str) -> None:
    """hash the specified file with each available hash and return stats"""

    hashes = get_available_hashes()
    max_len_hash = max([len(hash) for hash in hashes]) + 2

    hash_times = process_map(
        timed_get_hash,
        hashes,
        repeat(path),
        max_workers=4,
        chunksize=1,
        desc="Hashing Files...",
    )
    hash_times = {k: v for k, v in hash_times}
    hash_times = sorted(hash_times.items(), key=lambda x: x[1])

    click.echo("Order = fastest > slowest")
    for hash, elapsed_time in hash_times:
        click.echo(f"{hash.ljust(max_len_hash)} {elapsed_time :8.6f} sec")


@cli.command()
@click.option(
    "--test_path",
    "-tp",
    type=click.Path(),
    default=os.getcwd(),
    help="path where test directories and files will be created",
)
@click.option(
    "--numdirs",
    "-nd",
    type=click.INT,
    default=3,
    help="number of directories to make for the test",
)
@click.option(
    "--numfiles",
    "-nf",
    type=click.INT,
    default=3,
    help="number of files to make in each directory, spread through the directories",
)
@click.option(
    "--max_file_size",
    "-fs",
    type=click.INT,
    default=1024,
    help="file size to create in bytes",
)
def make_test_files(test_path: Path, numdirs: int, numfiles: int, max_file_size: int):
    """
    make test files to test 'duple scan' and 'duple rm'
    """

    os.chdir(test_path)
    file_sizes = [x for x in range(max_file_size)]
    # data = [os.urandom(file_size) for _ in range(int(numfiles/2))]
    data = [
        os.urandom(choice(file_sizes)) for _ in range(int((numfiles * numdirs) / 2))
    ]

    lennumdir = len(str(numdirs))
    lennumfiles = len(str(numfiles))

    for i in tqdm(range(numdirs), desc="making directories", position=0):
        leni = len(str(i))
        dir_path = str(
            Path(os.getcwd())
            .joinpath(f'folder_{"".ljust(lennumdir - leni, "0")}{i}')
            .absolute()
        )

        if not Path(dir_path).exists():
            os.mkdir(dir_path)

        for j in range(numfiles):
            lenj = len(str(j))
            file_name = str(
                Path(dir_path).joinpath(
                    f'file_{"".ljust(lennumfiles - lenj, "0")}{j}.txt'
                )
            )

            if Path(file_name).exists():
                continue

            with open(file_name, "wb") as f:
                f.write(choice(data))
