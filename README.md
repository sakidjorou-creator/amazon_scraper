# Amazon Scraper (mini-projet, séance 2)

Scraper Python en POO (architecture MVC) : Selenium + BeautifulSoup, stockage SQLite, export CSV, 3 statistiques.

**Site :** amazon.fr, catégorie High-Tech, avec 3 sous-catégories : smartphone, ordinateur portable, casque audio.
3 pages scrapées par catégorie (10 produits par page), soit 9 pages.

## Règles respectées
- `robots.txt` vérifié avant chaque page (le scraper refuse les pages interdites)
- pause de 4 s (+ aléa) entre requêtes, User-Agent identifiable
- arrêt immédiat si Amazon affiche un captcha
- aucune donnée personnelle collectée (titre, prix, note, photo uniquement)

## Installation et lancement
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
pytest
```
Google Chrome doit être installé. Modifie `USER_AGENT` dans `config.py` avec ton email.

## Résultats
- `data/produits.db` (SQLite), `data/images/` (photos)
- `exports/produits_*.csv`
- Statistiques en console : prix moyen, prix maximum, nombre par catégorie

## Structure
`models/` (Produit, Depot) · `views/` (console, export CSV) · `controllers/` (orchestration) · `scraper/` (navigateur Selenium, parsing, images)
