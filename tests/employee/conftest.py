import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.employee import get_employee_service
from app.main import app
from app.services.employee import EmployeeService

from typing import Generator


@pytest.fixture(scope="class", autouse=True)
def set_up_data(test_session: Session) -> Generator:
    def override_employee_service() -> EmployeeService:
        return EmployeeService(session=test_session)

    app.dependency_overrides[get_employee_service] = override_employee_service

    yield test_session
