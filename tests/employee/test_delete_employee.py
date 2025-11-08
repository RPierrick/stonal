from fastapi.testclient import TestClient


class TestRetriveEmployee:
    def test_retrive_employee_sucess(self, client: TestClient) -> None:
        response = client.delete(
            "/api/v1/employees/628",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response.status_code == 204

        response_get = client.get(
            "/api/v1/employees/628",
            headers={"Authorization": "Basic YWRtaW46MTIzNA==="},
        )

        assert response_get.status_code == 404

    def test_no_credentials(self, client: TestClient) -> None:
        response = client.delete(
            "/api/v1/employees/628",
        )

        assert response.status_code == 401
