"""
test/test_users.py
Tests for user API endpoints.
"""
import uuid

from fastapi import status


class TestUserAPI:
    """Test cases for User API endpoints."""

    def test_create_user(self, client, sample_user_data):
        response = client.post("/api/v1/users/", json=sample_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_create_duplicate_user(self, client):
        user_data = {"name": "John Doe", "email": "duplicate@example.com"}
        client.post("/api/v1/users/", json=user_data)
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    def test_get_user(self, client, sample_user_data):
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]

    def test_get_nonexistent_user(self, client):
        response = client.get("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_get_all_users(self, client, sample_user_data):
        user1 = sample_user_data.copy()
        user2 = {"name": "Jane Smith", "email": f"jane.smith.{uuid.uuid4().hex[:8]}@example.com"}

        resp1 = client.post("/api/v1/users/", json=user1)
        resp2 = client.post("/api/v1/users/", json=user2)

        assert resp1.status_code == status.HTTP_201_CREATED
        assert resp2.status_code == status.HTTP_201_CREATED

        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        all_users = response.json()

        test_users = [u for u in all_users if u["email"] in {user1["email"], user2["email"]}]
        assert len(test_users) == 2

    def test_update_nonexistent_user(self, client):
        update_data = {"name": "John Smith"}
        response = client.put("/api/v1/users/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_delete_user(self, client, sample_user_data):
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_user(self, client):
        response = client.delete("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_get_user_with_tasks(self, client, sample_user_data):
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        response = client.get(f"/api/v1/users/{user_id}/with-tasks")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert "tasks" in data
        assert isinstance(data["tasks"], list)
