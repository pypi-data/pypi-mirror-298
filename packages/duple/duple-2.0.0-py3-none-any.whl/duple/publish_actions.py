from duple.info import PYPROJECT, VERSION_PATH


def sync_version():
    version = PYPROJECT["tool"]["poetry"]["version"]

    with open(VERSION_PATH, "w") as f:
        f.write(f"__version__ = '{version}'")
