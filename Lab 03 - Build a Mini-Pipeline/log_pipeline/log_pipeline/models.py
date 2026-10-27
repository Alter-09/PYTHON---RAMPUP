"""Data models for log procedssing"""

from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True, frozen=True)
class LogEntry:
    """Inmutable Container for log event data.
    
    Using slots=True reduces memory footprint per instance, and frozen=True
    makes instance attributes immutable and hashable.
    """
    timestamp: str
    level: str
    message: str
