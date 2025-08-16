""" Test-friendly engine override """
from sqlalchemy.engine import Engine
from typing import Callable, Any


def override_engine(new_engine: Engine) -> Callable[[Callable[..., Any]],
                                                    Callable[..., Any]]:
    """
    Decorator that temporarily replaces `core.db.engine` with `new_engine`
    during the wrapped function execution. Useful in tests.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            from core.db import engine as original
            try:
                # monkey‑patch
                import sys
                sys.modules['core.db'].engine = new_engine
                return func(*args, **kwargs)
            finally:
                sys.modules['core.db'].engine = original
        return wrapper
    return decorator
