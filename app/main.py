from fastapi import FastAPI
from sqlalchemy import exc

from app.api.v1 import employee
from app.core.config import config
from app.core.custom_exceptions import UnreachableDatabase
from app.db.base import Base, engine


if not config.db_url.endswith("test"):
    try:
        Base.metadata.create_all(bind=engine)
    except exc.OperationalError as err:
        raise UnreachableDatabase("DB not reachable") from err


app = FastAPI(
    title="Stonal API",
    description="API for managing employees",
    version="0.1.0",
)

app.include_router(employee.app, prefix="/api/v1/employees", tags=["Employee"])
