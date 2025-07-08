import os
import sys

import pytest
from sqlalchemy import create_engine

# Import depuis app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal
from initialiser_items import init_magasins, init_products, init_users
from models import Base, Magasin, Product, Utilisateur


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_init_products():
    init_products()
    db = SessionLocal()
    produits = db.query(Product).all()
    db.close()
    assert len(produits) == 20
    assert produits[0].name.startswith("Produit")

def test_init_users():
    init_users()
    db = SessionLocal()
    users = db.query(Utilisateur).all()
    roles = set(user.role.value for user in users)
    db.close()
    assert len(users) == 3
    assert roles == {"employe", "gestionnaire", "responsable"}

def test_init_magasins():
    init_magasins()
    db = SessionLocal()
    magasins = db.query(Magasin).all()
    db.close()
    assert len(magasins) >= 1
    assert magasins[0].nom.startswith("Magasin")

