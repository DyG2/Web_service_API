from fastapi import APIRouter
from pydantic import BaseModel
from db import connexion
from datetime import date

router = APIRouter(tags=["Stock & Dashboard"])

class MajStock(BaseModel):
    quantite: int

@router.get("/stock")
def voir_stock():
    conn = connexion()
    rows = conn.execute("SELECT * FROM stock").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.put("/stock/{article}")
def maj_stock(article: str, data: MajStock):
    conn = connexion()
    conn.execute("UPDATE stock SET quantite=? WHERE article=?", (data.quantite, article))
    conn.commit()
    conn.close()
    return {"message": f"{article} → {data.quantite} unités ✓"}

@router.get("/dashboard")
def dashboard():
    conn = connexion()
    aujourd_hui = str(date.today())
    resa = conn.execute("SELECT * FROM reservations WHERE date=?", (aujourd_hui,)).fetchall()
    stock = conn.execute("SELECT * FROM stock").fetchall()
    conn.close()

    return {
        "date": aujourd_hui,
        "chambres_vendues": len(resa),
        "total_encaisse": sum(r["montant"] for r in resa if r["paye"] == 1),
        "total_restant": sum(r["montant"] for r in resa if r["paye"] == 0),
        "stock": [dict(s) for s in stock]
    }