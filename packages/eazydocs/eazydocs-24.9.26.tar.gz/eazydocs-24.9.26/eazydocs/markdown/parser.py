from re import findall


class Parser:
    """eazydocs.markdown.Parser

    Parses a markdown file into its methods and their params. The format of
    this markdown file is as defined by eazydocs.markdown.format.

    Args:
        string (str): String expression representing contents of a markdown file.
            This argument can be obtained using the method `read_md_file`
    """

    def __init__(self, string: str) -> None:

        self.string = string

        self.methods = dict()

        self.parse()

    def parse(self) -> None:
        methods = self._get_methods()
        self._get_method_params(methods)

    def _get_methods(self) -> list[str]:
        methods = findall(r"\<strong .+\>(.+)</strong>", self.string)
        return methods

    def _get_method_params(self, methods: list[str]) -> None:
        for method in methods:
            params = self._get_params(method)
            self.methods.update({method: params})

    def _get_params(self, method: str) -> dict:
        param_names = self._get_param_names(method)
        params = self._get_param_descriptions(param_names)
        return params

    def _get_param_names(self, method: str) -> list[str]:
        param_names = findall(rf"{method}-(.+)\'", self.string)
        param_names = [p for p in param_names if "-description" not in p]
        return param_names

    def _get_param_descriptions(self, param_names: list[str]) -> dict:
        params = dict()

        for param in param_names:
            description = findall(rf"{param}-description'>(.+)\.", self.string)
            if description != []:
                params.update({param: description[0]})
            else:
                params.update({param: None})

        return params
