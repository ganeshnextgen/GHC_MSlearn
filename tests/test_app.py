import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(app_module.activities)


def test_unregister_existing_participant():
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    updated = client.get("/activities").json()
    assert "michael@mergington.edu" not in updated["Chess Club"]["participants"]


def test_unregister_missing_participant():
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "ghost@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
