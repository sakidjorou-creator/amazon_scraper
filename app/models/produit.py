"""Modèle Produit (un livre)."""


class Produit:
    def __init__(self, titre, prix, stock, note, categorie, url, image_url="", image_path=""):
        self.titre = titre
        self.prix = prix          # float, en €
        self.stock = stock        # texte, ex. "In stock"
        self.note = note          # float de 0 à 5
        self.categorie = categorie
        self.url = url
        self.image_url = image_url
        self.image_path = image_path

    def en_dict(self):
        return dict(self.__dict__)

    def __repr__(self):
        return f"Produit({self.titre!r}, {self.prix}, {self.categorie!r})"
