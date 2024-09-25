from duple.__version__ import __version__
from pathlib import Path
import os
import sysconfig
import tomllib

PROJECT_ROOT = Path(__file__).parent.parent
PROJECT_TOML = PROJECT_ROOT.joinpath("pyproject.toml")
USER_SCRIPTS_PATH = sysconfig.get_path("scripts", f"{os.name}_user")
VERSION_PATH = Path(__file__).parent.joinpath("__version__.py")

if Path(PROJECT_TOML).exists():
    with PROJECT_TOML.open("rb") as toml_file:
        PYPROJECT = tomllib.load(toml_file)


def get_user_scripts_path():
    print()
    print()
    print(USER_SCRIPTS_PATH)
    print()
    print()
