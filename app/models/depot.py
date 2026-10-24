"""Dépôt SQLite : stockage et statistiques."""
import sqlite3
from pathlib import Path

from app.models.produit import Produit


class Depot:
    def __init__(self, chemin):
        Path(chemin).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(chemin))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS produits (
                url TEXT PRIMARY KEY, titre TEXT, prix REAL, stock TEXT,
                note REAL, categorie TEXT, image_url TEXT, image_path TEXT)"""
        )
        self.conn.commit()

    def ajouter(self, p):
        self.conn.execute(
            "INSERT OR REPLACE INTO produits VALUES (?,?,?,?,?,?,?,?)",
            (p.url, p.titre, p.prix, p.stock, p.note, p.categorie, p.image_url, p.image_path),
        )
        self.conn.commit()

    def vider(self):
        self.conn.execute("DELETE FROM produits")
        self.conn.commit()

    def tous(self):
        lignes = self.conn.execute(
            "SELECT * FROM produits ORDER BY categorie, titre"
        ).fetchall()
        return [Produit(**dict(l)) for l in lignes]

    # --- Statistiques ---
    def moyenne_prix(self):
        v = self.conn.execute("SELECT AVG(prix) FROM produits").fetchone()[0]
        return v or 0.0

    def maximum_prix(self):
        l = self.conn.execute(
            "SELECT titre, prix FROM produits ORDER BY prix DESC LIMIT 1"
        ).fetchone()
        return (l["titre"], l["prix"]) if l else ("-", 0.0)

    def nombre_par_categorie(self):
        l = self.conn.execute(
            "SELECT categorie, COUNT(*) n FROM produits GROUP BY categorie ORDER BY categorie"
        ).fetchall()
        return {r["categorie"]: r["n"] for r in l}

    def fermer(self):
        self.conn.close()
