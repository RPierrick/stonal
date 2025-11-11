from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import pytest

from app.db import Employee
import datetime
from typing import Generator


class TestCreateEmployee:
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
        test_session.query(Employee).filter(Employee.id == 1).delete()
        test_session.commit()

    def test_create_employee_sucess(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/employees",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
            json={
                "first_name": "string",
                "last_name": "string",
                "email": "user@example.com",
                "birth_date": "2025-11-08",
                "hire_date": "2025-11-08",
                "position": "Software Engineer",
                "salary": 2.12,
            },
        )

        assert response.status_code == 201
    
    def test_create_employee_negative_salary(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/employees",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
            json={
                "first_name": "string",
                "last_name": "string",
                "email": "user@example.com",
                "birth_date": "2025-11-08",
                "hire_date": "2025-11-08",
                "position": "Software Engineer",
                "salary": -2.12,
            },
        )

        assert response.status_code == 422
        
        response_body = response.json()
        assert response_body["detail"][0]["msg"] == "Value error, Salary cannot be a negative number"

    def test_create_employee_wrong_body(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/employees",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
            json={},
        )

        assert response.status_code == 422

    def test_create_employee_same_email(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/employees",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
            json={
                "first_name": "string",
                "last_name": "string",
                "email": "bruce.wayne@corp.com",
                "birth_date": "2025-11-08",
                "hire_date": "2025-11-08",
                "position": "Software Engineer",
                "salary": 2.12,
            },
        )

        assert response.status_code == 400

        response_body = response.json()

        assert response_body["detail"]["exception"] == "Unique Key Constraint Violation"

    def test_create_no_credentials(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/employees",
            headers={},
            json={},
        )

        assert response.status_code == 401
