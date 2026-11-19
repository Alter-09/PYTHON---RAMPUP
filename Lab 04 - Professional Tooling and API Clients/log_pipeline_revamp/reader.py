from contextlib import contextmanager
from typing import Generator, TextIO
from pathlib import Path
from log_pipeline_revamp.models import LogEntry

logger_reader = logging.getLogger("log_pipeline_revamp.reader")


def stream_log_lines(file_path: Path) -> Generator[str, None, None]:
    """Lee un archivo de log de forma perezosa línea por línea.

    Yields:
        str: Cada línea individual de texto no vacía del archivo.
    """
    if not file_path.exists():
        logger_reader.error("Intento de acceso a archivo inexistente: %s", file_path)
        raise ResourceNotFoundError(f"El archivo no existe en la ruta: {file_path}")

    logger_reader.info("Abriendo flujo de lectura perezosa para: %s", file_path)
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                yield clean_line
