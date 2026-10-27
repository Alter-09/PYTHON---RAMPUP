from contextlib import contextmanager
from typing import Generator, TextIO
from pathlib import Path
from log_pipeline.models import LogEntry

@contextmanager
def safe_open_log(file_path: Path) -> Generator[TextIO, None, None]:
    """Custom context manager protecting file resource handle. 
    
    Guarantees the file handle closes in a finally block even if an exception occurs. 
    
    Args:
        file_path: Path to the log file to open.
        
    Returns:
        Generator that yields the file handle.
    """
    if not file_path.exists(): 
        raise FileNotFoundError(f"Log file not found at: {file_path}") 
    file_handle = file_path.open(mode="r", encoding="utf-8") 
    try: 
        yield file_handle
    finally: 
        file_handle.close()


def iter_log_lines(file_path: Path) -> Generator[str, None, None]: 
    """
    Yield lines one by one without loading the entire file into memory (O(1) space).
    
    Args:
        file_path: Path to the log file to open.
        
    Returns:
        Generator that yields each line from the file.
    """
    with safe_open_log(file_path) as file: 
        for line in file: 
            yield line.strip()

