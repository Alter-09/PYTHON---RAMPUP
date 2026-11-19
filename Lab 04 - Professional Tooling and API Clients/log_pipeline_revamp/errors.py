class LogPipelineError(Exception):
    """Excepción base para todas las excepciones del paquete log_pipeline_revamp."""
    pass


class LogParseError(LogPipelineError):
    """Lanzada cuando una línea de log tiene un formato sintáctico inválido."""

    def __init__(self, line: str, reason: str) -> None:
        self.line = line
        self.reason = reason
        super().__init__(f"Error al parsear línea de log '{line}': {reason}")


class ResourceNotFoundError(LogPipelineError):
    """Lanzada cuando el archivo de log no existe en el sistema de archivos."""
    pass
