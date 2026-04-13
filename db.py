import sqlite3

def connexion():
    conn = sqlite3.connect("hotel.db")
    conn.row_factory = sqlite3.Row
    return conn

def creer_tables():
    conn = connexion()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS chambres (
        id INTEGER PRIMARY KEY,
        numero TEXT,
        categorie TEXT,
        prix REAL,
        statut TEXT DEFAULT 'propre'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        client TEXT,
        identite TEXT,
        chambre_id INTEGER,
        montant REAL,
        paye INTEGER DEFAULT 0,
        date TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS stock (
        article TEXT PRIMARY KEY,
        quantite INTEGER
    )""")

    #Donnée initiale
    if conn.execute("SELECT COUNT(*) FROM chambres").fetchone()[0] == 0:
        conn.executemany("INSERT INTO chambres (numero, categorie, prix) VALUES (?,?,?)", [
            ("101", "Standard", 50000),
            ("102", "Standard", 50000),
            ("201", "Suite Senior", 100000),
            ("301", "Suite Prestige", 180000),
        ])

    if conn.execute("SELECT COUNT(*) FROM stock").fetchone()[0] == 0:
        conn.executemany("INSERT INTO stock VALUES (?,?)", [
            ("gel_douche", 50),
            ("papier_hygienique", 50),
            ("pantoufle", 50),
            ("brosse_dent", 50),
        ])

    conn.commit()
    conn.close()