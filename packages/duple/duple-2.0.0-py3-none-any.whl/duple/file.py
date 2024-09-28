from dataclasses import dataclass, field
from pathlib import Path
import hashlib
from duple.status import Status


@dataclass
class File:
    path: Path
    status: Status = field(init=False, default=Status.NOT_ANALYZED)
    name: str = field(init=False, default="")
    namelength: int = field(init=False, default=0)
    twins: list = field(init=False, default=0)
    size: int = field(init=False, default=0)
    atime: float = field(init=False, default=0)
    ctime: float = field(init=False, default=0)
    mtime: float = field(init=False, default=0)
    hash: str = field(init=False, default="")
    depth: str = field(init=False, default=0)

    def get_available_option_attributes():
        result = ["depth", "namelength", "atime", "ctime", "mtime"]
        return result

    def calc_hash(self, hashalgo: str = ""):
        with open(self.path, "rb") as f:
            digest = hashlib.file_digest(f, hashalgo)
        self.hash = digest.hexdigest()
        return self

    def __post_init__(self):
        if isinstance(self.path, str):
            self.path = Path(self.path)

        self.depth = len(self.path.parents)
        self.name = self.path.name
        self.namelength = len(self.name)
        self.size = self.path.stat().st_size
        self.atime = self.path.stat().st_atime
        self.ctime = self.path.stat().st_ctime
        self.mtime = self.path.stat().st_mtime
