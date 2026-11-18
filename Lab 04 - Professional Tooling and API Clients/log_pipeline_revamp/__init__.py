"""Log processing pipeline package."""

from log_pipeline.models import LogEntry
from log_pipeline.decorators import timed, logged
from log_pipeline.reader import iter_log_lines, parse_logs, safe_open_log

__all__ = [
    "LogEntry",
    "timed",
    "logged",
    "iter_log_lines",
    "parse_logs",
    "safe_open_log",
]