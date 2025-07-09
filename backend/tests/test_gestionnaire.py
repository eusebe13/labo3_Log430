# tests/test_gestionnaire.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_afficher_rapports():
    response = client.get("/gestionnaire/rapports")
    assert response.status_code == 200

def test_generer_rapport():
    data = {"region": "Nord"}
    response = client.post("/gestionnaire/rapports", json=data)
    assert response.status_code == 200 or response.status_code == 400
