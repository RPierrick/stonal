from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import pytest

from app.db import Employee
import datetime
from typing import Generator


class TestListEmployee:
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

    def test_list_employee_sucess(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?offset=0&limit=50",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body == {
            "total": 2,
            "offset": 0,
            "limit": 50,
            "employees": [
                {
                    "first_name": "Bruce",
                    "last_name": "Wayne",
                    "email": "bruce.wayne@corp.com",
                    "birth_date": "1980-05-15",
                    "hire_date": "2010-06-01",
                    "position": "Software Engineer",
                    "salary": "80000.00",
                    "id": 626,
                },
                {
                    "first_name": "Clark",
                    "last_name": "Kent",
                    "email": "clark.kent@corp.com",
                    "birth_date": "1980-05-15",
                    "hire_date": "2010-06-01",
                    "position": "Marketing Coordinator",
                    "salary": "80000.00",
                    "id": 627,
                },
            ],
        }

    def test_list_employee_using_offset(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?offset=1&limit=50",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body["total"] == 1

    def test_list_employee_using_position(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?position=Marketing%20Coordinator",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body == {
            "total": 1,
            "offset": 0,
            "limit": 25,
            "employees": [
                {
                    "first_name": "Clark",
                    "last_name": "Kent",
                    "email": "clark.kent@corp.com",
                    "birth_date": "1980-05-15",
                    "hire_date": "2010-06-01",
                    "position": "Marketing Coordinator",
                    "salary": "80000.00",
                    "id": 627,
                },
            ],
        }

    def test_list_employee_using_false_position(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?position=Foo",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body == {"employees": [], "limit": 25, "offset": 0, "total": 0}

    def test_list_employee_using_min_max_salary(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?min_salary=0&max_salary=90000.00",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body["total"] == 2

    def test_list_employee_using_min_salary(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?min_salary=0",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body["total"] == 2

    def test_list_employee_using_max_salary(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/?max_salary=90000.00",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body["total"] == 2
