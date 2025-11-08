from fastapi.testclient import TestClient


class TestCreateEmployee:
    def test_create_employee_sucess(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/employees",
            json={
                "first_name": "string",
                "last_name": "string",
                "email": "user@example.com",
                "birth_date": "2025-11-08",
                "hire_date": "2025-11-08",
                "position": "string",
                "salary": 2.12,
            },
        )

        assert response.status_code == 201

    def test_create_employee_wrong_body(self, client: TestClient) -> None:
        response = client.post("/api/v1/employees", json={})

        assert response.status_code == 422
