from pathlib import Path

from .reader import Reader
from .parser import Parser
from .updater import Updater


def read_md_file(filename: str, filepath: str | Path = None) -> str:
    with Reader(filename, filepath) as f:
        contents = f.contents
    return contents


def get_methods(filename: str, filepath: str | Path = None) -> dict:
    contents = read_md_file(filename, filepath)
    parser = Parser(contents)
    methods = parser.methods
    return methods

def update_md_file(cls_or_method: object, filename: str, filepath: str | Path = None) -> None:
    Updater(cls_or_method, filename,filepath)
    
    