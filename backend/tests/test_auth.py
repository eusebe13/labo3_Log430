# tests/test_auth.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_connexion_valide():
    response = client.post("/connexion", json={"nom": "Bob", "mot_de_passe": "1234"})
    assert response.status_code == 200
    assert "token" in response.json()

def test_connexion_invalide():
    response = client.post("/connexion", json={"nom": "fake", "mot_de_passe": "wrong"})
    assert response.status_code == 401
