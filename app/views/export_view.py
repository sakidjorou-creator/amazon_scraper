"""Export CSV."""
import csv
from datetime import datetime


class ExportView:
    CHAMPS = ["titre", "prix", "stock", "note", "categorie", "url", "image_url", "image_path"]

    def __init__(self, dossier):
        self.dossier = dossier

    def exporter_csv(self, produits):
        self.dossier.mkdir(parents=True, exist_ok=True)
        chemin = self.dossier / f"produits_{datetime.now():%Y%m%d_%H%M%S}.csv"
        with open(chemin, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=self.CHAMPS)
            w.writeheader()
            for p in produits:
                w.writerow({c: getattr(p, c) for c in self.CHAMPS})
        return chemin
