from .cls import Cls
from .method import Method
from .param import Param


class Generator:
    def __init__(self, arg: Cls | Method) -> None:
        self.arg = arg

        self.parameters = "\n> Parameters\n\n"
        self.docs = str()
        self.table_of_contents: list[str] = list()
        self.method = arg.name

        self.get_docs()

    def get_docs(self) -> None:
        docs = str()
        if isinstance(self.arg, Cls):
            docs += f"## {self.arg.name}\n\n"

            if self.arg.methods is not None:
                method_docs = str()
                while self.arg.methods:
                    method: Method = self.arg.methods.pop(0)
                    self.table_of_contents.append(method.id)
                    generator = Generator(method)
                    method_docs += generator.docs

                docs += self._get_table_of_contents()
                docs += self._get_docs()
                docs += method_docs
            else:
                docs += self._get_docs()
        else:
            docs += self._get_docs()

        self.docs = docs

    def _get_function(self) -> str:
        template = "<strong id='{method_id}'>{method}</strong>("
        template = template.replace("{method_id}", self.arg.id).replace(
            "{method}", self.arg.name
        )
        while self.arg.params:
            param = self.arg.params.pop(0)
            # append to Parameters section
            self._append_param(param)
            # fmt param for function
            param = self._fmt_param(param)
            template += param

        template = template.rstrip(", ") + ")\n"

        return template

    def _fmt_param(self, param: Param) -> str:
        name = param.name
        default_arg = self._get_default_arg(param.default_arg)

        if default_arg is not None:
            template = f"<b>{name}</b><i>={default_arg}</i>, "
        else:
            template = f"<b>{name}</b>, "

        return template

    def _get_default_arg(self, arg: str | None) -> str:
        if arg is None:
            default_arg = None
        elif arg == "None":
            default_arg = "_NoDefault.no_default"
        else:
            default_arg = arg

        return default_arg

    def _append_param(self, param: Param) -> None:
        description = self._check_description(param.description)

        template = f"<ul style='list-style: none'>\n\t<li id='{self.method}-{param.name}'>\n"

        if param.default_arg is None:
            template += f"\t\t<b>{param.name} : <i>{param.arg_type}</i></b>\n"
        elif param.default_arg == "None":
            template += f"\t\t<b>{param.name} : <i>{param.arg_type}, optional</i></b>\n"
        else:
            template += f"\t\t<b>{param.name} : <i>{param.arg_type}, default {param.default_arg}</i></b>\n"

        template += f"\t\t<ul style='list-style: none'>\n\t\t\t<li id='{self.method}-{param.name}-description'>{description}</li>\n\t\t</ul>\n\t</li>\n</ul>\n"

        self.parameters += template

    def _check_description(self, string: str) -> str:
        if "`" in string:
            while "`" in string:
                string = string.replace("`", "<code>", 1).replace(
                    "`", "</code>", 1
                )

        return string

    def _get_docs(self) -> None:
        docs = str()
        docs += self._get_function()
        docs += f"\n{self.arg.summary}\n"
        docs += self.parameters
        docs += "\n<hr>\n"
        return docs

    def _get_table_of_contents(self) -> str:
        table_of_contents = f"- [Parameters](#{self.arg.name})\n"
        table_of_contents += "- Methods:\n"

        for method in self.table_of_contents:
            name = method.replace("-", "_")
            link = f"  - [{name}](#{method})\n"
            table_of_contents += link

        table_of_contents += "\n"

        return table_of_contents

    @property
    def link(self) -> str:
        template = f"[`{self.arg.name}`](#{self.arg.id})"
        return template
