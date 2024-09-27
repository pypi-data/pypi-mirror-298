from inspect import getmembers, isfunction, ismethod
from re import findall, DOTALL

from eazydocs.core.method import Method


class Cls:
    def __init__(self, cls: object) -> None:
        self.name: str = cls.__name__
        self.methods = list()
        self.id = self.name.replace("_", "-")
        self.docstring = cls.__doc__

        for name, member in getmembers(cls):
            if ismethod(member) or isfunction(member):
                if name == "__init__":
                    method = Method(member)
                    self.params = method.params
                    self._get_summary()
                elif not name.startswith("_"):
                    self.methods.append(Method(member))

    def __repr__(self) -> str:
        return f"name:{self.name}\nmethods:{self.methods}\n"

    def _get_summary(self) -> None:
        regex: str = findall(r"(.*)Args:", self.docstring, DOTALL)[0]
        regex = regex.strip()

        if "\n" in regex:
            regex = regex.split("\n")
            regex = [rgx.strip() for rgx in regex]
            summary = " ".join(regex)
        elif regex != "":
            summary = regex
        else:
            summary = None

        self.summary = summary
