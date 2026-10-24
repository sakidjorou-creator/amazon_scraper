"""Extraction des données depuis le HTML d'Amazon (sélecteurs CSS)."""
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

SEL_RESULTAT = 'div[data-component-type="s-search-result"]'


def convertir_prix(texte):
    """'1 299,00 €' -> 1299.0 ; '199,99€' -> 199.99 ; None si introuvable."""
    t = (texte or "").replace("\xa0", " ").replace("\u202f", " ")
    m = re.search(r"\d[\d .,]*", t)
    if not m:
        return None
    s = m.group().strip().replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def convertir_note(texte):
    """'4,5 sur 5 étoiles' -> 4.5 ; 0.0 si absent."""
    m = re.search(r"\d+(?:[.,]\d+)?", texte or "")
    return float(m.group().replace(",", ".")) if m else 0.0


def parser_page(html, url_page, categorie, limite=None):
    """Retourne la liste des produits (dicts) d'une page de résultats."""
    soup = BeautifulSoup(html, "html.parser")
    produits = []
    for bloc in soup.select(SEL_RESULTAT):
        titre_el = bloc.select_one("h2 span") or bloc.select_one("h2")
        prix_el = bloc.select_one("span.a-price span.a-offscreen")
        if not titre_el or not prix_el:
            continue  # bloc publicitaire ou produit sans prix
        prix = convertir_prix(prix_el.get_text())
        if prix is None:
            continue
        asin = bloc.get("data-asin")
        lien = bloc.select_one("h2 a") or bloc.select_one("a.a-link-normal")
        if asin:
            url = urljoin(url_page, "/dp/" + asin)
        elif lien and lien.get("href"):
            url = urljoin(url_page, lien["href"])
        else:
            continue
        note_el = bloc.select_one("span.a-icon-alt")
        img = bloc.select_one("img.s-image")
        produits.append({
            "titre": titre_el.get_text(strip=True),
            "prix": prix,
            "stock": "Disponible",
            "note": convertir_note(note_el.get_text() if note_el else ""),
            "categorie": categorie,
            "url": url,
            "image_url": img["src"] if img and img.get("src") else "",
        })
        if limite and len(produits) >= limite:
            break
    return produits
