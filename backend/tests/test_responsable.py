# tests/test_responsable.py
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_consulter_stock():
    response = client.get("/api/v1/responsable/stock")
    assert response.status_code == 200

def test_get_alertes_rupture():
    response = client.get("/api/v1/responsable/alertes-rupture")
    assert response.status_code == 200

def test_get_produits_par_magasin():
    response = client.get("/api/v1/responsable/magasin/1/produits")
    assert response.status_code in (200, 404)


def test_reapprovisionnement_approuver():
    # Suppose une demande existe avec ID 1
    response = client.post("/api/v1/responsable/reapprovisionner/1/approuver")
    assert response.status_code in (200, 404, 400)
