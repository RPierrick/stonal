from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions

from app.db.base import Base
from app.main import app

from sqlalchemy_utils import create_database, drop_database, database_exists


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def test_session() -> Generator:
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/test"
    if database_exists(db_url):
        drop_database(db_url)
    create_database(db_url)

    engine = create_engine(
        db_url,
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        close_all_sessions()
        session.close()
        connection.close()
