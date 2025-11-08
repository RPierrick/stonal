import datetime

import pytest
from sqlalchemy.orm import Session

from app.api.v1.employee import get_employee_service
from app.db import Employee
from app.main import app
from app.services.employee import EmployeeService

from typing import Generator


@pytest.fixture(scope="session", autouse=True)
def set_up_data(test_session: Session) -> Generator:
    test_session.add(
        Employee(
            id=626,
            first_name="Bruce",
            last_name="Wayne",
            email="bruce.wayne@corp.com",
            birth_date=datetime.date(1980, 5, 15),
            hire_date=datetime.date(2010, 6, 1),
            position="The Dark Knight",
            salary=8000000,
        )
    )
    test_session.add(
        Employee(
            id=627,
            first_name="Clark",
            last_name="Kent",
            email="clark.kent@corp.com",
            birth_date=datetime.date(1980, 5, 15),
            hire_date=datetime.date(2010, 6, 1),
            position="The Son of Krypton",
            salary=8000000,
        )
    )
    test_session.commit()

    def override_employee_service() -> EmployeeService:
        return EmployeeService(session=test_session)

    app.dependency_overrides[get_employee_service] = override_employee_service

    yield test_session
