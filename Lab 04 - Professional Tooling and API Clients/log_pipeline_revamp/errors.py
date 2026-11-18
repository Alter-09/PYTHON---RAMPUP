"""Custom Exception Classes for the log_pipeline Package"""

class LogPipelineError(Exception):
    """Excepción base para todas las excepciones del paquete log_pipeline."""
    pass

class LogParseError(LogPipelineError):
    """"""
    def __init__ (self, line: str, reason: str):
        self.line = line
        self.reason = reason
        super().__init__(f"Error al parsear linea '{line}': {reason} de log")

class ResourceNotFoundError(LogPipelineError):
    """"""
    pass
