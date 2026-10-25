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