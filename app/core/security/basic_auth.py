import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import config


security = HTTPBasic()


def basic_authorization(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    is_username_correct = secrets.compare_digest(
        credentials.username.encode(), config.fast_api_user.encode()
    )
    is_password_correct = secrets.compare_digest(
        credentials.password.encode(), config.fast_api_password.encode()
    )

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
