"""Navigateur Selenium poli : robots.txt, pauses, détection de captcha."""
import random
import time
from urllib import robotparser
from urllib.parse import urljoin

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CaptchaError(Exception):
    """Amazon demande un captcha : on arrête de scraper."""


class Navigateur:
    def __init__(self, site_url, user_agent, headless=False, delai=4.0,
                 timeout=15, respecter_robots=True, page_load_timeout=40):
        self.delai = delai
        self.timeout = max(timeout, 25)
        self.http_timeout = timeout
        self.user_agent = user_agent
        self.respecter_robots = respecter_robots
        self.robots = robotparser.RobotFileParser()
        self._charger_robots(site_url)

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.page_load_strategy = "eager"
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--lang=fr-FR")
        options.add_argument("--window-size=1366,900")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(page_load_timeout)

    def _charger_robots(self, site_url):
        try:
            r = requests.get(urljoin(site_url, "/robots.txt"),
                             headers={"User-Agent": self.user_agent}, timeout=self.http_timeout)
            self.robots.parse(r.text.splitlines() if r.status_code == 200 else [])
        except requests.RequestException:
            self.robots.parse([])

    def autorise(self, url):
        return (not self.respecter_robots) or self.robots.can_fetch(self.user_agent, url)

    def _pause(self):
        time.sleep(self.delai + random.uniform(0, 1.5))

    def _captcha(self):
        src = self.driver.page_source.lower()
        return "captcha" in src or "validatecaptcha" in src

    def _accepter_cookies(self):
        """Ferme la bannière de cookies d'Amazon si elle est affichée."""
        try:
            boutons = self.driver.find_elements(By.ID, "sp-cc-accept")
            if boutons:
                boutons[0].click()
                time.sleep(1.5)
        except Exception:
            pass

    def ouvrir(self, url, selecteur_attendu):
        if not self.autorise(url):
            raise PermissionError(f"robots.txt interdit : {url}")
        self._pause()
        try:
            self.driver.get(url)
        except TimeoutException:
            try:
                self.driver.execute_script("window.stop();")
            except Exception:
                pass
        self._accepter_cookies()
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selecteur_attendu)))
            time.sleep(2)
        except TimeoutException:
            if self._captcha():
                raise CaptchaError("Amazon a affiché un captcha.")
        return self.driver.page_source

    def fermer(self):
        self.driver.quit()