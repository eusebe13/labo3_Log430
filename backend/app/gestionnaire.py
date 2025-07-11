from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
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
@router.get("/rapports/consolide", status_code=status.HTTP_200_OK)
def rapport_consolide(db: Session = Depends(get_db)):
    try:
        ventes_par_magasin = db.query(
            Magasin.nom,
            func.sum(Vente.prix_total).label("chiffre_affaires")
        ).join(Magasin, Magasin.id == Vente.magasin_id).group_by(Magasin.nom).all()

        produits_plus_vendus = db.query(
            Product.name,
            func.sum(Vente.quantite).label("total_vendu")
        ).join(Product, Product.id == Vente.produit_id).group_by(Product.name).order_by(
            func.sum(Vente.quantite).desc()).limit(5).all()

        stocks = db.query(
            Product.name,
            func.coalesce(StockCentral.quantite, 0).label("stock_central")
        ).outerjoin(StockCentral, StockCentral.produit_id == Product.id).all()

        return {
            "ventes_par_magasin": [{"magasin": v[0], "chiffre_affaires": v[1]} for v in ventes_par_magasin],
            "produits_plus_vendus": [{"produit": p[0], "quantite_vendue": p[1]} for p in produits_plus_vendus],
            "stocks_centrals": [{"produit": s[0], "stock": s[1]} for s in stocks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

# === TABLEAU DE BORD ===
@router.get("/dashboard", status_code=status.HTTP_200_OK)
def tableau_de_bord(db: Session = Depends(get_db)):
    try:
        chiffres = db.query(
            Magasin.nom,
            func.sum(Vente.prix_total)
        ).join(Magasin, Magasin.id == Vente.magasin_id).group_by(Magasin.nom).all()

        ruptures = db.query(
            Product.name,
            Magasin.nom,
            ProduitParMagasin.quantite
        ).join(ProduitParMagasin, Product.id == ProduitParMagasin.produit_id)\
         .join(Magasin, Magasin.id == ProduitParMagasin.magasin_id)\
         .filter(ProduitParMagasin.quantite < 5).all()

        surstocks = db.query(
            Product.name,
            Magasin.nom,
            ProduitParMagasin.quantite
        ).join(ProduitParMagasin, Product.id == ProduitParMagasin.produit_id)\
         .join(Magasin, Magasin.id == ProduitParMagasin.magasin_id)\
         .filter(ProduitParMagasin.quantite > 100).all()

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

# === RAPPORT BASIQUE (EXISTANT) ===
@router.get("/rapports", status_code=status.HTTP_200_OK)
def afficher_rapports(db: Session = Depends(get_db)):
    try:
        rapports = db.query(RapportTendance).all()
        return [{"id": r.id, "region": r.region, "total_ventes": r.total_ventes} for r in rapports]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des rapports : {str(e)}")

@router.post("/rapports", status_code=status.HTTP_201_CREATED)
def generer_rapport(data: RapportCreate, db: Session = Depends(get_db)):
    try:
        total_ventes = db.query(func.sum(Vente.prix_total))\
            .join(Magasin, Magasin.id == Vente.magasin_id)\
            .filter(Magasin.region == data.region).scalar() or 0.0

        rapport = RapportTendance(region=data.region, total_ventes=total_ventes)
        db.add(rapport)
        db.commit()
        db.refresh(rapport)

        return {
            "message": f"Rapport pour la région {data.region} créé.",
            "rapport_id": rapport.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du rapport : {str(e)}")
