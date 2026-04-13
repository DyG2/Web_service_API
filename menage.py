from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import connexion

router = APIRouter(prefix="/menage", tags=["Menage"])

class FinMenage(BaseModel):
    chambre_id: int
    femme_menage: str

@router.get("/a-faire")
def chambres_sales():
    conn = connexion()
    rows = conn.execute("SELECT * FROM chambres WHERE statut='sale'").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("/terminer")
def terminer(data: FinMenage):
    conn = connexion()
    chambre = conn.execute("SELECT * FROM chambres WHERE id=?", (data.chambre_id,)).fetchone()
    if not chambre:
        raise HTTPException(404, "Chambre introuvable")
    if chambre["statut"] != "sale":
        raise HTTPException(400, "Cette chambre n'est pas sale")

    conn.execute("UPDATE chambres SET statut='propre' WHERE id=?", (data.chambre_id,))
    conn.commit()
    conn.close()
    return {"message": f"Chambre {chambre['numero']} propre — réceptionniste notifiée ✓"}

@router.put("/chambre/{id}/sale")
def marquer_sale(id: int):
    conn = connexion()
    conn.execute("UPDATE chambres SET statut='sale' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Chambre marquée sale ✓"}