from pathlib import Path


def check_filename(filename: str) -> str:
    if not filename.endswith(".md"):
        filename = filename.strip()
        filename += ".md"

    return filename


def set_path(filename: str, filepath: str | Path) -> Path:
    if isinstance(filepath, str):
        path = Path(filepath)
        filepath = path.joinpath(filename)
    else:
        filepath = Path(filename)

    return filepath
