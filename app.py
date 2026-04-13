from fastapi import FastAPI
from db import creer_tables
import chambres, reservations, menage, stock

app = FastAPI(title="Hotel API")

@app.on_event("startup")
def startup():
    creer_tables()

app.include_router(chambres.router)
app.include_router(reservations.router)
app.include_router(menage.router)
app.include_router(stock.router)