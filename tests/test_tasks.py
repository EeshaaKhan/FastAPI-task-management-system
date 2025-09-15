"""
Tests for task API endpoints.
"""
from fastapi import status


class TestTaskAPI:
    """Test cases for Task API endpoints."""

    def test_create_task(self, client, sample_user_data, sample_task_data):
        """Test creating a new task."""
        # Create user first
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        # Create task
        response = client.post(f"/api/v1/users/{user_id}/tasks/", json=sample_task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["status"] == "TODO"
        assert data["description"] == sample_task_data["description"]
        assert data["user_id"] == user_id

    def test_update_nonexistent_task(self, client):
        """Test updating a task that doesn't exist."""
        update_data = {"title": "Updated title"}
        response = client.put("/api/v1/tasks/999", json=update_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_update_task_status(self, client, sample_user_data, sample_task_data):
        """Test updating task status."""
        # Create user and task
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        task_response = client.post(f"/api/v1/users/{user_id}/tasks/", json=sample_task_data)
        task_id = task_response.json()["id"]

        # Update status
        status_data = {"status": "DONE"}
        response = client.patch(f"/api/v1/tasks/{task_id}/status", json=status_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "DONE"

    def test_delete_task(self, client, sample_user_data, sample_task_data):
        """Test deleting a task."""
        # Create user and task
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        task_response = client.post(f"/api/v1/users/{user_id}/tasks/", json=sample_task_data)
        task_id = task_response.json()["id"]

        # Delete task
        response = client.delete(f"/api/v1/tasks/{task_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist."""
        response = client.delete("/api/v1/tasks/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_get_user_task_stats(self, client, sample_user_data, sample_task_data):
        """Test getting task statistics for a user."""
        # Create user
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        # Create tasks with different statuses
        tasks_data = [
            {"title": "Task 1", "description": "First task"},
            {"title": "Task 2", "description": "Second task"},
            {"title": "Task 3", "description": "Third task"},
        ]

        task_ids = []
        for task_data in tasks_data:
            task_response = client.post(f"/api/v1/users/{user_id}/tasks/", json=task_data)
            task_ids.append(task_response.json()["id"])

        # Update statuses
        client.patch(f"/api/v1/tasks/{task_ids[1]}/status", json={"status": "IN_PROGRESS"})
        client.patch(f"/api/v1/tasks/{task_ids[2]}/status", json={"status": "DONE"})

        # Get stats
        response = client.get(f"/api/v1/users/{user_id}/tasks/stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user_id"] == user_id
        assert data["total_tasks"] == 3
        assert data["todo_tasks"] == 1
        assert data["in_progress_tasks"] == 1
        assert data["done_tasks"] == 1
        assert data["completion_rate"] == 33.33

    def test_get_tasks_by_status(self, client, sample_user_data):
        """Test filtering tasks by status."""
        # Create user
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        # Create tasks
        task1_response = client.post(f"/api/v1/users/{user_id}/tasks/", json={"title": "Task 1"})
        task2_response = client.post(f"/api/v1/users/{user_id}/tasks/", json={"title": "Task 2"})

        # Update one task status
        task2_id = task2_response.json()["id"]
        client.patch(f"/api/v1/tasks/{task2_id}/status", json={"status": "DONE"})

        # Filter by TODO status
        response = client.get(f"/api/v1/users/{user_id}/tasks/?status_filter=TODO")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "TODO"

        # Filter by DONE status
        response = client.get(f"/api/v1/users/{user_id}/tasks/?status_filter=DONE")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "DONE"

    def test_create_task_for_nonexistent_user(self, client, sample_task_data):
        """Test creating a task for a user that doesn't exist."""
        response = client.post("/api/v1/users/999/tasks/", json=sample_task_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_get_task(self, client, sample_user_data, sample_task_data):
        """Test getting a task by ID."""
        # Create user and task
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        task_response = client.post(f"/api/v1/users/{user_id}/tasks/", json=sample_task_data)
        task_id = task_response.json()["id"]
        # Get task
        response = client.get(f"/api/v1/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task_data["title"]
        assert data["user_id"] == user_id

    def test_get_nonexistent_task(self, client):
        """Test getting a task that doesn't exist."""
        response = client.get("/api/v1/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_get_user_tasks(self, client, sample_user_data, sample_task_data):
        """Test getting all tasks for a user."""
        # Create user
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        # Create multiple tasks
        task_data_1 = sample_task_data.copy()
        task_data_2 = {"title": "Another task", "description": "Second task"}
        client.post(f"/api/v1/users/{user_id}/tasks/", json=task_data_1)
        client.post(f"/api/v1/users/{user_id}/tasks/", json=task_data_2)
        # Get user tasks
        response = client.get(f"/api/v1/users/{user_id}/tasks/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert all(task["user_id"] == user_id for task in data)

    def test_update_task(self, client, sample_user_data, sample_task_data):
        """Test updating a task."""
        # Create user and task
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        task_response = client.post(f"/api/v1/users/{user_id}/tasks/", json=sample_task_data)
        task_id = task_response.json()["id"]

        # Update task
        update_data = {"title": "Updated task title", "status": "IN_PROGRESS"}
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated task title"
        assert data["status"] == "IN_PROGRESS"
        assert data["description"] == sample_task_data["description"]
        assert data["id"] == task_id
        assert data["user_id"] == user_id
