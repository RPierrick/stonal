from fastapi.testclient import TestClient


class TestRetriveEmployee:
    def test_retrive_employee_sucess(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/626",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 200

        response_body = response.json()

        assert response_body == {
            "id": 626,
            "salary": "80000.00",
            "first_name": "Bruce",
            "last_name": "Wayne",
            "email": "bruce.wayne@corp.com",
            "position": "Software Engineer",
            "birth_date": "1980-05-15",
            "hire_date": "2010-06-01",
        }

    def test_retrive_employee_not_found(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/0",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 404

    def test_no_credentials(self, client: TestClient) -> None:
        response = client.get(
            "/api/v1/employees/626",
        )

        assert response.status_code == 401
