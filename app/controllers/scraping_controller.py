"""Contrôleur : orchestre scraper, dépôt et vues."""
import config
from app.models.depot import Depot
from app.scraper.amazon_scraper import AmazonScraper
from app.scraper.driver import CaptchaError, Navigateur
from app.scraper.images import telecharger_image
from app.views.console_view import ConsoleView
from app.views.export_view import ExportView


class ScrapingController:
    def __init__(self):
        self.vue = ConsoleView()
        self.export = ExportView(config.EXPORT_DIR)
        self.depot = Depot(config.DB_PATH)

    def _quotas(self):
        """Répartit MAX_PRODUITS_TOTAL entre les catégories (ex. 10 -> 4, 3, 3)."""
        total = getattr(config, "MAX_PRODUITS_TOTAL", 10)
        base, reste = divmod(total, len(config.CATEGORIES))
        return [base + (1 if i < reste else 0) for i in range(len(config.CATEGORIES))]

    def executer(self):
        navigateur = Navigateur(config.AMAZON_URL, config.USER_AGENT, config.HEADLESS,
                                config.DELAI_ENTRE_REQUETES, config.TIMEOUT,
                                config.RESPECTER_ROBOTS,
                                getattr(config, "PAGE_LOAD_TIMEOUT", 40))
        scraper = AmazonScraper(navigateur, config.AMAZON_URL, getattr(config, "PAGES_MAX", 1))
        self.depot.vider()
        try:
            for (nom, terme), quota in zip(config.CATEGORIES.items(), self._quotas()):
                self.vue.message(f"Scraping de la catégorie : {nom} ({quota} produits)")
                try:
                    for produit in scraper.scraper_categorie(nom, terme, quota):
                        if config.TELECHARGER_IMAGES and produit.image_url:
                            try:
                                produit.image_path = telecharger_image(
                                    produit, config.IMAGES_DIR, config.USER_AGENT,
                                    config.DELAI_IMAGES, config.TIMEOUT)
                            except Exception as e:
                                self.vue.message(f"  image ignorée ({e})")
                        self.depot.ajouter(produit)
                except CaptchaError as e:
                    self.vue.message(f"  {e} Arrêt du scraping.")
                    break
                except Exception as e:
                    self.vue.message(f"  erreur sur {nom} : {e}")
        finally:
            navigateur.fermer()

        produits = self.depot.tous()
        self.vue.message(f"\n{scraper.pages_visitees} pages scrapées, {len(produits)} produits.")
        if not produits:
            self.vue.message("Aucun produit récupéré (captcha, robots.txt ou sélecteurs à ajuster).")
            self.depot.fermer()
            return
        self.vue.afficher_produits(produits)
        chemin = self.export.exporter_csv(produits)
        self.vue.message(f"\nCSV enregistré : {chemin}")
        self.vue.afficher_stats(self.depot.moyenne_prix(), self.depot.maximum_prix(),
                                self.depot.nombre_par_categorie())
        self.depot.fermer()
