from fastapi.testclient import TestClient


class TestCreateEmployee:
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
                "position": "string",
                "salary": 2.12,
            },
        )

        assert response.status_code == 201

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
                "position": "string",
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
