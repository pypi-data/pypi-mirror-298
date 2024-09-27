from pathlib import Path

from eazydocs.core import Generator
from eazydocs.core.common import check_filename, set_path


class Writer:
    def __init__(
        self,
        contents: str | Generator,
        filename: str,
        filepath: str | Path = None,
    ) -> None:
        self.contents = contents

        filename = check_filename(filename)

        if filepath is not None:
            if isinstance(filepath, str):
                filepath = Path(filepath)

            filename = filepath.joinpath(filename)
        else:
            filename = Path(filename)

        self.filename = filename

        if isinstance(contents, Generator):
            contents = contents.docs

    def write(self) -> None:
        with open(self.filename, "w") as f:
            f.write(self.contents)
