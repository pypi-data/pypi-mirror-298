from duple.info import PYPROJECT, VERSION_PATH
from pathlib import Path


def sync_version():
    version = PYPROJECT["tool"]["poetry"]["version"]

    with open(VERSION_PATH, "w") as f:
        f.write(f"__version__ = '{version}'")
