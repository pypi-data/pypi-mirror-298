from pathlib import Path
from typing import Literal

from eazydocs.core.common import check_filename, set_path


class Reader:
    def __init__(
        self,
        filename: str,
        filepath: str | Path = None,
    ) -> None:
        filename = check_filename(filename)

        if filepath is not None:
            filename = set_path(filename, filepath)

        print(filename)

        self.filename = filename

    # Context Manager Interface
    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Literal[False]:
        return False

    def load(self, filename: str = None, filepath: str | Path = None) -> None:
        if self.filename is None:
            raise TypeError("Invalid argument provided for 'filename'")
        elif filename is not None:
            self.filename = filename

        with open(self.filename, "r") as f:
            self.contents = f.read()

    def _check_filetype(self, filename: str) -> bool:
        if "." in filename:
            parts = filename.split(".")

            ext = parts[-1]  # assume last . is the file extension

            if "md" not in ext:
                return False

        return True
