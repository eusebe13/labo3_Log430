from typing import Dict, List

from fastapi import APIRouter, Body, HTTPException
from app.database import SessionLocal
from app.models import Magasin, Product, ProduitParMagasin, Vente, StockCentral, Reaprovisionnement

router = APIRouter()


@router.get("/produits")
def consulter_product():
    session = SessionLocal()
    produits = session.query(Product).all()
    session.close()
    return [{"id": p.id, "name": p.name, "price": p.price} for p in produits]

@router.get("/magasin/{magasin_id}/produits")
def consulter_produit_par_magasin(magasin_id: int):
    session = SessionLocal()
    try:
        produits = session.query(ProduitParMagasin).filter_by(magasin_id=magasin_id).all()
        if not produits:
            return {"message": "Aucun produit trouvé pour ce magasin."}
        return [{"produit": p.produit.name, "quantite": p.quantite} for p in produits]
    finally:
        session.close()

@router.get("/stock/{produit_id}/magasin/{magasin_id}")
def verifier_stock(produit_id: int, magasin_id: int):
    session = SessionLocal()
    try:
        stock = session.query(ProduitParMagasin).filter_by(produit_id=produit_id, magasin_id=magasin_id).first()
        produit = session.query(Product).get(produit_id)
        magasin = session.query(Magasin).get(magasin_id)

        if not produit or not magasin:
            raise HTTPException(status_code=404, detail="Produit ou magasin introuvable.")

        if not stock:
            return {"message": f"{produit.name} ({magasin.nom}) : stock non disponible."}

        return {
            "produit": produit.name,
            "magasin": magasin.nom,
            "quantite": stock.quantite
        }
    finally:
        session.close()

@router.get("/stockcentral/produits")
def consulter_stock_central_complet():
    session = SessionLocal()
    try:
        produits = session.query(Product).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "stock_central": p.stock_central.quantite if p.stock_central else 0
            } for p in produits
        ]
    finally:
        session.close()

@router.post("/acheter/{magasin_id}")
def acheter_produit(magasin_id: int, liste_produit: List[Dict] = Body(...)):
    '''
    liste_produit = [
        {"produit_id": 1, "quantite": 2},
        {"produit_id": 3, "quantite": 1},
    ]
    '''
    session = SessionLocal()
    try:
        messages = []
        for item in liste_produit:
            produit_id = item.get("produit_id")
            quantite = item.get("quantite", 0)

            stock = session.query(ProduitParMagasin).filter_by(produit_id=produit_id, magasin_id=magasin_id).first()
            produit = session.query(Product).get(produit_id)

            if not produit or not stock:
                messages.append(f"Produit ID {produit_id} indisponible.")
                continue

            if stock.quantite < quantite:
                messages.append(f"{produit.name} : stock insuffisant ({stock.quantite} dispo).")
                continue

            stock.quantite -= quantite

            vente = Vente(
                produit_id=produit_id,
                magasin_id=magasin_id,
                quantite=quantite,
                prix_total=produit.price * quantite
            )
            session.add(vente)
            messages.append(f"{produit.name} : achat de {quantite} unités confirmé.")

        session.commit()
        return {"resultats": messages}
    except Exception as e:
        session.rollback()
        return {"erreur": str(e)}
    finally:
        session.close()

@router.post("/reapprovisionner/produit/{produit_id}/quantite/{quantite}/magasin/{magasin_id}")
def demander_reapprovisionnement(produit_id: int, quantite: int, magasin_id: int):
    session = SessionLocal()
    try:
        produit = session.query(Product).get(produit_id)
        magasin = session.query(Magasin).get(magasin_id)

        if not produit or not magasin:
            raise HTTPException(status_code=404, detail="Produit ou magasin introuvable.")

        demande_existante = session.query(Reaprovisionnement).filter_by(
            produit_id=produit_id, magasin_id=magasin_id, approuved=False
        ).first()

        if demande_existante:
            return {"message": f"Une demande de réapprovisionnement pour {produit.name} existe déjà."}

        demande = Reaprovisionnement(
            produit_id=produit_id,
            magasin_id=magasin_id,
            quantite=quantite,
            approuved=False
        )
        session.add(demande)
        session.commit()

        return {"message": f"Demande de réapprovisionnement pour {produit.name} envoyée."}

    except Exception as e:
        session.rollback()
        return {"erreur": f"Erreur lors de la demande : {str(e)}"}
    finally:
        session.close()
