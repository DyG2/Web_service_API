from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import connexion
from datetime import date

router = APIRouter(prefix="/reservations", tags=["Reservations"])

ARTICLES = ["gel_douche", "papier_hygienique", "pantoufle", "brosse_dent"]

class NouvelleReservation(BaseModel):
    client: str
    identite: str
    chambre_id: int

@router.get("/")
def liste():
    conn = connexion()
    rows = conn.execute("SELECT * FROM reservations").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("/")
def reserver(data: NouvelleReservation):
    conn = connexion()

    # S'il existe une chambre propre
    chambre = conn.execute("SELECT * FROM chambres WHERE id=?", (data.chambre_id,)).fetchone()
    if not chambre:
        raise HTTPException(404, "Chambre introuvable")
    if chambre["statut"] != "propre":
        raise HTTPException(400, f"Chambre non disponible — statut: {chambre['statut']}")

    # Si stock insuffissant
    for article in ARTICLES:
        row = conn.execute("SELECT quantite FROM stock WHERE article=?", (article,)).fetchone()
        if row["quantite"] < 1:
            raise HTTPException(400, f"Stock insuffisant: {article}")

    # Creation de reservation
    conn.execute(
        "INSERT INTO reservations (client, identite, chambre_id, montant, date) VALUES (?,?,?,?,?)",
        (data.client, data.identite, data.chambre_id, chambre["prix"], str(date.today()))
    )
    reservation_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # On descend le stock et on occupe la chambre
    for article in ARTICLES:
        conn.execute("UPDATE stock SET quantite = quantite - 1 WHERE article=?", (article,))
    conn.execute("UPDATE chambres SET statut='occupee' WHERE id=?", (data.chambre_id,))

    conn.commit()
    conn.close()
    return {"reservation_id": reservation_id, "montant": chambre["prix"], "message": "Réservation créée ✓"}

@router.post("/{id}/payer")
def payer(id: int):
    conn = connexion()
    conn.execute("UPDATE reservations SET paye=1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Paiement enregistré ✓"}