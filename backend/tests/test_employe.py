# tests/test_employe.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_consulter_produits():
    response = client.get("/api/v1/employe/produits")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_verifier_stock():
    response = client.get("/api/v1/employe/stock/1/magasin/1")
    assert response.status_code in (200, 404)

def test_acheter_produits():
    data = [
        {"produit_id": 1, "quantite": 1}
    ]
    response = client.post("/api/v1/employe/acheter/1", json=data)
    assert response.status_code in (200, 400)
