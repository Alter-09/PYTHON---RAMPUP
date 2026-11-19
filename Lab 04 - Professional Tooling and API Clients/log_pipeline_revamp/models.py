"""Data models for log procedssing"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LogEntry:
    """Modelo inmutable de un evento de log individual."""

    timestamp: datetime
    level: str
    service: str
    message: str

    @classmethod
    def from_raw_line(cls, line: str) -> "LogEntry":
        """Factory method que transforma una línea bruta de texto en una instancia de LogEntry."""
        clean = line.strip()
        if not clean:
            raise LogParseError(line, "Línea vacía no procesable")

        parts = clean.split(" ", 3)
        if len(parts) < 4:
            raise LogParseError(line, "Número insuficiente de campos (se esperan mínimo 4)")

        raw_date, raw_time, raw_level, rest = parts
        try:
            timestamp = datetime.strptime(f"{raw_date} {raw_time}", "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise LogParseError(line, f"Formato de fecha u hora inválido: {e}") from e

        level = raw_level.strip("[]").upper()
        if ":" not in rest:
            raise LogParseError(line, "Falta el delimitador 'service: message'")

        service, message = rest.split(":", 1)
        return cls(
            timestamp=timestamp,
            level=level,
            service=service.strip(),
            message=message.strip(),
        )

