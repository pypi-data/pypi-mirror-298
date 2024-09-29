from functools import wraps
import logging
from typing import Any, Callable


def log_exceptions(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(wrapped=func)
    def wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            logging.exception(msg=f"Exception in {func.__name__}")
            raise

    return wrapper


def log_function_call(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(wrapped=func)
    def wrapper(*args: Any, **kwargs: dict[str, Any]) -> Any:
        logging.info(msg=f"Calling function {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
