from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import pytest

from app.db import Employee
import datetime
from typing import Generator


class TestDeleteEmployee:
    @pytest.fixture(autouse=True)
    def setUp(self, test_session: Session) -> Generator:
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
        test_session.commit()
        yield
        test_session.query(Employee).filter(Employee.id == 626).delete()
        test_session.commit()

    def test_delete_employee_sucess(self, client: TestClient) -> None:
        response = client.delete(
            "/api/v1/employees/626",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 204

        response_get = client.get(
            "/api/v1/employees/626",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response_get.status_code == 404

    def test_no_credentials(self, client: TestClient) -> None:
        response = client.delete(
            "/api/v1/employees/626",
        )

        assert response.status_code == 401

    def test_delete_employee_sucess_2(self, client: TestClient) -> None:
        response = client.delete(
            "/api/v1/employees/626",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 204

        response_get = client.get(
            "/api/v1/employees/626",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response_get.status_code == 404
