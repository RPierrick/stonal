from fastapi.testclient import TestClient


class TestUpdateEmployee:
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
                "position": "The Dark Knight",
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
            "position": "The Dark Knight",
            "birth_date": "1980-05-15",
            "hire_date": "2010-06-01",
        }

    def test_update_employee_not_found(self, client: TestClient) -> None:
        response = client.get("/api/v1/employees/0", headers={"Authorization": "Basic YWRtaW46MTIzNA==="},)

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
                "position": "The Dark Knight",
                "birth_date": "1980-05-15",
                "hire_date": "2010-06-01",
            },
        )

        assert response.status_code == 400

    def test_no_credentials(self, client: TestClient) -> None:
        response = client.get("/api/v1/employees/0",)

        assert response.status_code == 401
