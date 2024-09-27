from inspect import Parameter, _empty
from re import match
from types import UnionType


class Param:
    def __init__(self, s: Parameter | tuple) -> None:
        self.s = s

        if isinstance(s, tuple):
            self._from_match()
        elif isinstance(s, Parameter):
            self._from_signature()

    def _from_match(self) -> None:
        # param.name
        self.name = self.s[0]
        # param.arg_type
        self.arg_type = self.s[1].replace(", optional", "")
        # param.default_arg & param.description
        arg = self.s[2]
        default_arg = match(r"(.+) Defaults to (.+).", arg)

        if default_arg:
            self.description = default_arg.group(1)
            self.default_arg = default_arg.group(2)
        else:
            self.default_arg = None
            self.description = arg

    def _from_signature(self) -> None:
        self.name = self.s.name

        if isinstance(self.s.annotation, UnionType):
            arg_type = str(self.s.annotation)
        else:
            arg_type = self.s.annotation.__name__

        self.arg_type = arg_type

        if self.s.default is _empty:
            default_arg = None
        else:
            default_arg = self.s.default

        self.default_arg = default_arg

        self.description = "_description_"

    def _from_dict(self) -> None:
        self.name = self.s[0]

        d: dict = self.s[1]

        self.arg_type = d["arg_type"]
        self.default_arg = d["default_arg"]
        self.description = d["description"]

    # def __repr__(self) -> str:
    #     return f"name: {self.name}\narg_type: {self.arg_type}\ndefault_arg: {self.default_arg}\ndescription: {self.description}"
