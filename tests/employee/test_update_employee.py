from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import pytest

from app.db import Employee
import datetime
from typing import Generator


class TestUpdateEmployee:
    @pytest.fixture(autouse=True)
    def init_data(self, test_session: Session) -> Generator:
        test_session.add(
            Employee(
                id=626,
                first_name="Bruce",
                last_name="Wayne",
                email="bruce.wayne@corp.com",
                birth_date=datetime.date(1980, 5, 15),
                hire_date=datetime.date(2010, 6, 1),
                position="Software Engineer",
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
                position="Marketing Coordinator",
                salary=8000000,
            )
        )
        test_session.commit()
        yield
        test_session.query(Employee).filter(Employee.id == 626).delete()
        test_session.query(Employee).filter(Employee.id == 627).delete()
        test_session.commit()

    def test_update_employee_sucess(self, client: TestClient) -> None:
        """Only change the salary"""
        response = client.patch(
            "/api/v1/employees/626",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
            json={
                "salary": "0",
                "first_name": "Bruce",
                "last_name": "Wayne",
                "email": "bruce.wayne@corp.com",
                "position": "Software Engineer",
                "birth_date": "1980-05-15",
                "hire_date": "2010-06-01",
            },
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body == {
            "id": 626,
            "salary": "0.00",
            "first_name": "Bruce",
            "last_name": "Wayne",
            "email": "bruce.wayne@corp.com",
            "position": "Software Engineer",
            "birth_date": "1980-05-15",
            "hire_date": "2010-06-01",
        }

    def test_update_employee_not_found(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/0",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 404

    def test_update_employee_email_already_use(self, client: TestClient) -> None:
        response = client.patch(
            "/api/v1/employees/627",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
            json={
                "salary": "0",
                "first_name": "Bruce",
                "last_name": "Wayne",
                "email": "bruce.wayne@corp.com",
                "position": "Software Engineer",
                "birth_date": "1980-05-15",
                "hire_date": "2010-06-01",
            },
        )

        assert response.status_code == 400

    def test_no_credentials(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/0",
        )

        assert response.status_code == 401
