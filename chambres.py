from fastapi import APIRouter
from db import connexion

router = APIRouter(prefix="/chambres", tags=["Chambres"])

@router.get("/")
def toutes_les_chambres():
    conn = connexion()
    rows = conn.execute("SELECT * FROM chambres").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.get("/propres")
def chambres_disponibles():
    conn = connexion()
    rows = conn.execute("SELECT * FROM chambres WHERE statut='propre'").fetchall()
    conn.close()
    return [dict(r) for r in rows]