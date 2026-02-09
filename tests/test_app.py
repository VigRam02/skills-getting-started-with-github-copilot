from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test.user@example.com"

    # Ensure email is not present before test
    data_before = client.get("/activities").json()
    participants = data_before[activity]["participants"]
    if email in participants:
        participants.remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant added
    data_after = client.get("/activities").json()
    assert email in data_after[activity]["participants"]

    # Unregister
    resp2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp2.status_code == 200
    assert "Unregistered" in resp2.json().get("message", "")

    # Verify removed
    data_final = client.get("/activities").json()
    assert email not in data_final[activity]["participants"]
