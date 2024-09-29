from duple.info import PYPROJECT, VERSION_PATH, APP_NAME_PATH, LOGGING_CONFIGURATION_PATH, LOGS_PATH
import json
import os
from pathlib import Path


def sync_version():
    version = PYPROJECT["tool"]["poetry"]["version"]
    message = f'__version__ = "{version}"'
    with open(VERSION_PATH, "w") as f:
        f.write(message)
    return message


def sync_logging_level() -> str:
    log_level = PYPROJECT["tool"]["duple"]["logging_level"]
    message = f"LOGGING_LEVEL = {log_level}"
    with open(LOGGING_CONFIGURATION_PATH, "r") as f:
        config = json.load(f)

    config["loggers"]["root"]["level"] = f"{log_level}"

    with open(LOGGING_CONFIGURATION_PATH, "w") as f:
        json.dump(config, f, indent=4)

    return message


def sync_application_name() -> str:
    app_name = PYPROJECT["tool"]["poetry"]["name"]
    message = f'APP_NAME = "{app_name}"'
    with open(APP_NAME_PATH, "w") as f:
        f.write(message)
    return message


def delete_logs() -> str:
    files = os.listdir(LOGS_PATH)
    for file in files:
        p = Path(LOGS_PATH).joinpath(file)
        p.unlink()

    p = Path(LOGS_PATH).joinpath("log.jsonl")
    with open(p, "a"):
        pass

    p = p.parent.joinpath("log.log")
    with open(p, "a"):
        pass

    return f"Deleted Log Files: {files}"


def sync_with_pyproject() -> str:
    results = list()
    results.append(sync_version())
    # results.append(sync_logging_level())
    results.append(sync_application_name())
    return results
