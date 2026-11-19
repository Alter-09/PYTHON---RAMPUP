
logger_filters = logging.getLogger("log_pipeline_revamp.filters")


def parse_log_entries(lines: Iterator[str]) -> Generator[LogEntry, None, None]:
    """Convierte un flujo de líneas de texto en un flujo perezoso de LogEntry."""
    for line in lines:
        try:
            yield LogEntry.from_raw_line(line)
        except LogParseError as err:
            logger_filters.warning("Omite línea corrupta en el pipeline: %s", err)


def filter_by_level(entries: Iterator[LogEntry], level: str) -> Generator[LogEntry, None, None]:
    """Filtra un flujo perezoso de LogEntry manteniendo solo el nivel especificado."""
    target_level = level.upper()
    for entry in entries:
        if entry.level == target_level:
            yield entry


def filter_by_service(entries: Iterator[LogEntry], service_name: str) -> Generator[LogEntry, None, None]:
    """Filtra un flujo perezoso de LogEntry por nombre de servicio exacto."""
    target_service = service_name.lower()
    for entry in entries:
        if entry.service.lower() == target_service:
            yield entry
