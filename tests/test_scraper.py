import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.depot import Depot
from app.models.produit import Produit
from app.scraper.parsing import convertir_note, convertir_prix, parser_page

HTML = """
<div data-component-type="s-search-result" data-asin="B0TEST0001">
  <img class="s-image" src="https://m.media-amazon.com/images/I/a.jpg">
  <h2><a href="/x/dp/B0TEST0001"><span>Smartphone Test 128 Go</span></a></h2>
  <span class="a-icon-alt">4,5 sur 5 étoiles</span>
  <span class="a-price"><span class="a-offscreen">1 299,00 €</span></span>
</div>
<div data-component-type="s-search-result" data-asin="B0TEST0002">
  <h2><span>Sans prix</span></h2>
</div>
"""


def test_prix():
    assert convertir_prix("1 299,00 €") == 1299.0
    assert convertir_prix("199,99€") == 199.99
    assert convertir_prix("rien") is None


def test_note():
    assert convertir_note("4,5 sur 5 étoiles") == 4.5
    assert convertir_note("") == 0.0


def test_parsing():
    produits = parser_page(HTML, "https://www.amazon.fr/s?k=smartphone", "Smartphone")
    assert len(produits) == 1
    p = produits[0]
    assert p["titre"] == "Smartphone Test 128 Go" and p["prix"] == 1299.0 and p["note"] == 4.5
    assert p["url"] == "https://www.amazon.fr/dp/B0TEST0001"


def test_stats(tmp_path):
    d = Depot(tmp_path / "t.db")
    d.ajouter(Produit("A", 10.0, "Disponible", 4.0, "X", "u1"))
    d.ajouter(Produit("B", 30.0, "Disponible", 4.5, "X", "u2"))
    d.ajouter(Produit("C", 20.0, "Disponible", 3.0, "Y", "u3"))
    assert d.moyenne_prix() == 20.0
    assert d.maximum_prix() == ("B", 30.0)
    assert d.nombre_par_categorie() == {"X": 2, "Y": 1}
