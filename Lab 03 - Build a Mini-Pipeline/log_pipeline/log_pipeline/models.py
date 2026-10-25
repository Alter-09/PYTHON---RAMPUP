from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True, frozen=True)
class LogEntry:
    """Inmutable Container for log event data."""
    timestamp: str
    level: str
    message: str
