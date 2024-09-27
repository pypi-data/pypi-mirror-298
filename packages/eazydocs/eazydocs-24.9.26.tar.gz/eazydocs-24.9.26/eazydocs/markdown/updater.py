from inspect import isclass, isfunction, ismethod
from pathlib import Path
from types import FunctionType

from eazydocs.core.common import check_filename, set_path
from eazydocs.core import Generator, Method

from .reader import Reader
from .parser import Parser
from .writer import Writer


class Updater:
    def __init__(
        self,
        method: FunctionType | Method,
        filename: str,
        filepath: str | Path = None,
    ) -> None:
        if isclass:
            raise TypeError(
                f"Invalid argument of {type(method)} provided for 'method'. Expected {FunctionType}"
            )
        elif not isfunction or not ismethod:
            raise TypeError(
                f"Invalid argument of {type(method)} provided for 'method'. Expected {FunctionType}"
            )

        filename = check_filename(filename)

        if filepath is not None:
            filename = set_path(filename, filepath)

        self.filename = filename

        self._get_current_docs()

        self.arg = Method(method)
        self._update_method()

    def _update_method(self) -> None:
        generator = Generator(self.arg)
        docs = generator.docs

        if self._is_new_method(self.arg.name):
            # raise ValueError(f"Unable to find {self.arg.name} in {self.filename}. If this is a new method, ")
            new_docs = f"{self.current_docs}\n{docs}"
            self._create_markdown(new_docs)
        else:
            self._trim_old_method(self.arg.name, docs)

    def _get_current_docs(self) -> None:
        with Reader(self.filename) as f:
            self.current_docs = f.contents

        parser = Parser(self.current_docs)
        self.current_methods = parser.methods

    def _is_new_method(self, method: str) -> bool:
        if self.current_methods.get(method) is None:
            return True
        return False

    def _create_markdown(self, contents: str) -> None:
        writer = Writer(contents, self.filename)
        writer.write()

    def _trim_old_method(self, method: str, method_docs: str) -> str:
        start, end = self._find_method_docs(method)
        before, after = self._get_before_after_docs(start, end)
        new_docs = f"{before}\n\n{method_docs}\n{after}"

        self._create_markdown(new_docs)

    def _find_method_docs(self, method: str) -> tuple[int, int]:
        start = self.current_docs.find(method) - (len(method) + 14)
        end = self.current_docs[start:].find("<hr>")

        return (start, end)

    def _get_before_after_docs(self, start: int, end: int) -> tuple[str, str]:
        before = self.current_docs[:start].strip()
        after = self.current_docs[(start + end) :].strip()

        return (before, after)
