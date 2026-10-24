"""Téléchargement des photos produits."""
import re
import time
from pathlib import Path

import requests


def nom_fichier(produit):
    base = re.sub(r"[^a-zA-Z0-9]+", "_", produit.titre).strip("_")[:50] or "image"
    asin = produit.url.rstrip("/").split("/")[-1]
    return f"{base}_{asin}.jpg"


def telecharger_image(produit, dossier, user_agent, delai=0.5, timeout=15):
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / nom_fichier(produit)
    if not chemin.exists():
        time.sleep(delai)
        rep = requests.get(produit.image_url, headers={"User-Agent": user_agent}, timeout=timeout)
        rep.raise_for_status()
        chemin.write_bytes(rep.content)
    return str(chemin)
