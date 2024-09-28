import os
import sysconfig
from pathlib import Path

import tomllib

PROJECT_ROOT = Path(__file__).parent.parent
PROJECT_TOML = PROJECT_ROOT.joinpath("pyproject.toml")
USER_SCRIPTS_PATH = sysconfig.get_path("scripts", f"{os.name}_user")
VERSION_PATH = Path(__file__).parent.joinpath("__version__.py")

if Path(PROJECT_TOML).exists():
    with PROJECT_TOML.open("rb") as toml_file:
        PYPROJECT = tomllib.load(toml_file)
