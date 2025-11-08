from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException

from app.core.custom_exceptions import (
    BadRequestError,
    IntegrityError,
    NotFoundError,
    UniqueConstraintError,
    UnreachableDatabase,
)


def exception_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        try:
            result = func(*args, **kwargs)
            return result
        except (
            BadRequestError,
            IntegrityError,
            NotFoundError,
            UniqueConstraintError,
            UnreachableDatabase,
        ) as e:
            raise HTTPException(
                status_code=e.status_code,
                detail={"exception": e.err, "message": str(e)},
            ) from e

    return wrapper
