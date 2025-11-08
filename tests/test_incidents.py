def test_create_incident(client):
    payload = {"description": "Самокат #42 не в сети", "source": "operator"}
    r = client.post("/incidents", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["description"] == payload["description"]
    assert data["status"] == "new"
    assert data["source"] == "operator"
    assert "created_at" in data

def test_list_incidents_with_status_filter(client):
    client.post("/incidents", json={"description": "A", "source": "operator"})
    client.post(
        "/incidents",
        json={"description": "B", "source": "monitoring", "status": "investigating"},
    )

    r = client.get("/incidents", params={"status": "investigating"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["description"] == "B"
    assert items[0]["status"] == "investigating"

def test_update_status_404_if_not_found(client):
    r = client.patch("/incidents/999/status", json={"status": "resolved"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Incident not found"

def test_update_status_success(client):
    created = client.post("/incidents", json={"description": "C", "source": "partner"})
    incident_id = created.json()["id"]

    r = client.patch(f"/incidents/{incident_id}/status", json={"status": "resolved"})
    assert r.status_code == 200
    assert r.json()["status"] == "resolved"
