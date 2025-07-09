from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Magasin, Product, ProduitParMagasin, RapportTendance, StockCentral, Vente
from app.schemas import RapportCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === RAPPORT CONSOLIDÉ ===
@router.get("/rapports/consolide")
def rapport_consolide(db: Session = Depends(get_db)):
    # Total des ventes par magasin
    ventes_par_magasin = db.query(
        Magasin.nom,
        func.sum(Vente.prix_total).label("chiffre_affaires")
    ).join(Magasin, Magasin.id == Vente.magasin_id).group_by(Magasin.nom).all()

    # Produits les plus vendus
    produits_plus_vendus = db.query(
        Product.name,
        func.sum(Vente.quantite).label("total_vendu")
    ).join(Product, Product.id == Vente.produit_id).group_by(Product.name).order_by(func.sum(Vente.quantite).desc()).limit(5).all()

    # Stocks restants par produit
    stocks = db.query(
        Product.name,
        func.coalesce(StockCentral.quantite, 0).label("stock_central")
    ).outerjoin(StockCentral, StockCentral.produit_id == Product.id).all()

    return {
        "ventes_par_magasin": [{"magasin": v[0], "chiffre_affaires": v[1]} for v in ventes_par_magasin],
        "produits_plus_vendus": [{"produit": p[0], "quantite_vendue": p[1]} for p in produits_plus_vendus],
        "stocks_centrals": [{"produit": s[0], "stock": s[1]} for s in stocks]
    }

# === TABLEAU DE BORD ===
@router.get("/dashboard")
def tableau_de_bord(db: Session = Depends(get_db)):
    # Chiffre d’affaires par magasin
    chiffres = db.query(
        Magasin.nom,
        func.sum(Vente.prix_total)
    ).join(Magasin, Magasin.id == Vente.magasin_id).group_by(Magasin.nom).all()

    # Alertes de rupture : stock < 5
    ruptures = db.query(
        Product.name,
        Magasin.nom,
        ProduitParMagasin.quantite
    ).join(ProduitParMagasin, Product.id == ProduitParMagasin.produit_id)\
     .join(Magasin, Magasin.id == ProduitParMagasin.magasin_id)\
     .filter(ProduitParMagasin.quantite < 5).all()

    # Surstock : stock > 100
    surstocks = db.query(
        Product.name,
        Magasin.nom,
        ProduitParMagasin.quantite
    ).join(ProduitParMagasin, Product.id == ProduitParMagasin.produit_id)\
     .join(Magasin, Magasin.id == ProduitParMagasin.magasin_id)\
     .filter(ProduitParMagasin.quantite > 100).all()

    # Ventes hebdomadaires (7 derniers jours)
    il_y_a_7_jours = datetime.utcnow() - timedelta(days=7)
    tendances = db.query(
        Product.name,
        func.sum(Vente.quantite).label("vendus_cette_semaine")
    ).join(Product, Product.id == Vente.produit_id)\
     .filter(Vente.date >= il_y_a_7_jours)\
     .group_by(Product.name)\
     .order_by(func.sum(Vente.quantite).desc())\
     .limit(5).all()

    return {
        "chiffre_affaires_par_magasin": [{"magasin": c[0], "montant": c[1]} for c in chiffres],
        "ruptures": [{"produit": r[0], "magasin": r[1], "quantite": r[2]} for r in ruptures],
        "surstocks": [{"produit": s[0], "magasin": s[1], "quantite": s[2]} for s in surstocks],
        "tendances_hebdo": [{"produit": t[0], "quantite_vendue": t[1]} for t in tendances]
    }

# === RAPPORT BASIQUE (DÉJÀ PRÉSENT) ===
@router.get("/rapports")
def afficher_rapports(db: Session = Depends(get_db)):
    rapports = db.query(RapportTendance).all()
    return [{"id": r.id, "region": r.region, "total_ventes": r.total_ventes} for r in rapports]

@router.post("/rapports")
def generer_rapport(data: RapportCreate, db: Session = Depends(get_db)):
    total_ventes = db.query(func.sum(Vente.prix_total))\
        .join(Magasin, Magasin.id == Vente.magasin_id)\
        .filter(Magasin.region == data.region).scalar() or 0.0

    rapport = RapportTendance(region=data.region, total_ventes=total_ventes)
    db.add(rapport)
    db.commit()
    db.refresh(rapport)
    return {"message": f"Rapport pour la région {data.region} créé.", "rapport_id": rapport.id}
