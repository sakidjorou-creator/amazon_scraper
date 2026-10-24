"""Paramètres du projet."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

AMAZON_URL = "https://www.amazon.fr/"
# catégorie (pour les statistiques) -> terme de recherche
CATEGORIES = {
    "Smartphone": "smartphone",
    "Ordinateur portable": "ordinateur portable",
    "Casque audio": "casque audio",
}

HEADLESS = False                 # False = on voit le navigateur (moins de blocages)
PAGES_MAX = 2                   # pages max par catégorie
MAX_PRODUITS_PAR_PAGE = 10       # on garde les N premiers produits de chaque page
DELAI_ENTRE_REQUETES = 4.0       # secondes (politesse, + petit aléa)
DELAI_IMAGES = 0.5
TIMEOUT = 15
RESPECTER_ROBOTS = True
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "IIT-ScraperEtudiant/1.0 (projet scolaire; contact: sakidjorou@gmail.com)"
)
TELECHARGER_IMAGES = True

DB_PATH = BASE_DIR / "data" / "produits.db"
IMAGES_DIR = BASE_DIR / "data" / "images"
EXPORT_DIR = BASE_DIR / "exports"
