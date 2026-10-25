from contextlib import contextmanager
from typing import Generator, TextIO
from pathlib import Path

@contextmanager
def safe_open_log(file_path: Path) -> Generator[TextIO, None, None]:
    """Custom context generator for safe file reading."""
    f = open(file_path, mode="r", encoding="utf-8")
    try:
        yield f
    finally:
        f.close()
