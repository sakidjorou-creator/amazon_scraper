"""Scraper orienté objet pour Amazon (pages de résultats de recherche)."""
import time
from pathlib import Path
from urllib.parse import quote_plus

from app.models.produit import Produit
from app.scraper.parsing import SEL_RESULTAT, parser_page

DEBUG_DIR = Path(__file__).resolve().parents[2] / "data"


class AmazonScraper:
    def __init__(self, navigateur, site_url, pages_max=1):
        self.navigateur = navigateur
        self.site_url = site_url
        self.pages_max = pages_max
        self.pages_visitees = 0

    def url_recherche(self, terme, page):
        return f"{self.site_url}s?k={quote_plus(terme)}&page={page}"

    def _lire_page(self, nom, url, limite):
        """Ouvre la page et extrait les produits ; 1 nouvel essai si la page est vide."""
        html = self.navigateur.ouvrir(url, SEL_RESULTAT)
        produits = parser_page(html, url, nom, limite)
        if not produits:
            time.sleep(5)
            html = self.navigateur.ouvrir(url, SEL_RESULTAT)
            produits = parser_page(html, url, nom, limite)
        if not produits:
            DEBUG_DIR.mkdir(parents=True, exist_ok=True)
            (DEBUG_DIR / f"debug_{nom.replace(' ', '_')}.html").write_text(html, encoding="utf-8")
        return produits

    def scraper_categorie(self, nom, terme, quota):
        """Génère au plus `quota` Produit pour la catégorie."""
        compte = 0
        for page in range(1, self.pages_max + 1):
            if compte >= quota:
                break
            url = self.url_recherche(terme, page)
            produits = self._lire_page(nom, url, quota - compte)
            self.pages_visitees += 1
            for d in produits:
                yield Produit(**d)
                compte += 1