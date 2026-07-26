"""
API contract tests — these mirror what frontend/src/api.ts does:

  listIssues   → GET    /api/v1/issues/
  createIssue  → POST   /api/v1/issues/
  updateIssue  → PUT    /api/v1/issues/{id}
  deleteIssue  → DELETE /api/v1/issues/{id}

If these pass, the React client and backend agree on the HTTP contract.
"""

from fastapi.testclient import TestClient


def test_list_issues_empty(client: TestClient) -> None:
    response = client.get("/api/v1/issues/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_issue(client: TestClient) -> None:
    payload = {
        "title": "Broken login",
        "description": "Users cannot sign in with Google",
        "priority": "high",
    }
    response = client.post("/api/v1/issues/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["priority"] == "high"
    assert body["status"] == "open"  # server sets default
    assert "id" in body


def test_create_issue_rejects_short_title(client: TestClient) -> None:
    response = client.post(
        "/api/v1/issues/",
        json={"title": "ab", "description": "long enough description", "priority": "low"},
    )
    assert response.status_code == 422  # Pydantic validation error


def test_get_issue_by_id(client: TestClient) -> None:
    created = client.post(
        "/api/v1/issues/",
        json={
            "title": "Missing favicon",
            "description": "Browser tab shows no icon",
            "priority": "low",
        },
    ).json()

    response = client.get(f"/api/v1/issues/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_issue_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/issues/does-not-exist")
    assert response.status_code == 404


def test_update_issue(client: TestClient) -> None:
    created = client.post(
        "/api/v1/issues/",
        json={
            "title": "Slow dashboard",
            "description": "Takes 5 seconds to load",
            "priority": "medium",
        },
    ).json()

    response = client.put(
        f"/api/v1/issues/{created['id']}",
        json={"status": "in_progress", "priority": "high"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"
    assert body["title"] == "Slow dashboard"  # unchanged fields kept


def test_delete_issue(client: TestClient) -> None:
    created = client.post(
        "/api/v1/issues/",
        json={
            "title": "Typo on homepage",
            "description": "Spelling error in hero text",
            "priority": "low",
        },
    ).json()

    delete_response = client.delete(f"/api/v1/issues/{created['id']}")
    assert delete_response.status_code == 204

    list_response = client.get("/api/v1/issues/")
    assert list_response.json() == []


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
