"""Affichage console."""


class ConsoleView:
    def message(self, texte):
        print(texte)

    def afficher_produits(self, produits, limite=15):
        print(f"\n{'Titre':45} {'Prix':>8} {'Note':>5}  Catégorie")
        print("-" * 80)
        for p in produits[:limite]:
            titre = p.titre if len(p.titre) <= 44 else p.titre[:41] + "..."
            print(f"{titre:45} {p.prix:>7.2f}€ {p.note:>5.1f}  {p.categorie}")
        if len(produits) > limite:
            print(f"... et {len(produits) - limite} autres (voir le CSV)")

    def afficher_stats(self, moyenne, maximum, par_categorie):
        print("\n=== STATISTIQUES ===")
        print(f"1. Prix moyen : {moyenne:.2f} €")
        print(f"2. Prix maximum : {maximum[1]:.2f} €  ({maximum[0]})")
        print("3. Nombre de produits par catégorie :")
        for cat, n in par_categorie.items():
            print(f"   - {cat} : {n}")
