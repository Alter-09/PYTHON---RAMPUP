from typing import Callable, Any, TypeVar
import functools
import logging

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """Decorador para medir el tiempo de ejecución de funciones usando logging."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import time
        logger = logging.getLogger(func.__module__)
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        logger.info("Función '%s' ejecutada en %.4f segundos.", func.__qualname__, elapsed)
        return result
    return wrapper  # type: ignore[return-value]


def log_execution(level: int = logging.DEBUG) -> Callable[[F], F]:
    """Decorador parametrizado para registrar llamadas a funciones y sus argumentos."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__module__)
            logger.log(level, "Ejecutando %s | args=%s kwargs=%s", func.__qualname__, args, kwargs)
            try:
                result = func(*args, **kwargs)
                logger.log(level, "%s finalizó con éxito.", func.__qualname__)
                return result
            except Exception as e:
                logger.error("Error durante la ejecución de %s: %s", func.__qualname__, e, exc_info=True)
                raise
        return wrapper  # type: ignore[return-value]
    return decorator

