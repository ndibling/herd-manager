from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_and_basic_flow():
    # Seed org should exist indirectly; check animals list call
    r = client.get("/api/animals")
    assert r.status_code == 200
    # Create minimal animal
    r = client.post("/api/animals", data={"species":"cow","name":"Daisy"})
    assert r.status_code == 200
    animal_id = r.json()["id"]
    # Add treatment
    r = client.post(f"/api/animals/{animal_id}/treatments", data={"date":"2025-01-01","category":"shot","name":"Rabies"})
    assert r.status_code == 200
    # Pedigree
    r = client.get(f"/api/animals/{animal_id}/pedigree?generations=4")
    assert r.status_code == 200
