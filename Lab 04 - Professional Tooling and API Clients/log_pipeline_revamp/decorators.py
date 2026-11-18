import functools
import time
from typing import Callable, Any

def timed(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator made for measurement and report of execution time.
    
    Args:
        func: Function to be decorated.
        
    Returns:
        Wrapper function that measures and reports execution time.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"Function '{func.__name__}' executed in {elapsed:.4f} seconds.")
        return result
    return wrapper

def logged(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that logs function call parameters and return value.
    
    Args:
        func: Function to be decorated.
        
    Returns:
        Wrapper function that logs function call parameters and return value.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOGGED] Calling '{func.__name__}' with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOGGED] '{func.__name__}' returned: {result}")
        return result
    return wrapper