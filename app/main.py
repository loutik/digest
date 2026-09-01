# Logique
import time
import os
# Server web
import threading
import http.server
import socketserver
# Modules internes
from grabber import fetch_data
from builder import build_html
from logger import log

# Variables

UPDATE_TIME = int(os.getenv("UPDATE_TIME", 120))
PORT = int(os.getenv("PORT", 8000))
MINIFLUX_DOMAIN = os.getenv("MINIFLUX_DOMAIN")
MINIFLUX_TOKEN = os.getenv("MINIFLUX_TOKEN")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(SCRIPT_DIR, "var", "html")

def web_server():
    os.chdir(WEB_DIR)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        log.info(f"Serveur web en écoute sur le port {PORT}.")
        httpd.serve_forever()

def orchestrator():
    log.info("Démarrage du service d'orchestration.")

    while True:
        log.info("Début d'un nouveau cycle de synchronisation.")

        feeds, entries = fetch_data(MINIFLUX_DOMAIN, MINIFLUX_TOKEN)

        if feeds is not None:
            log.info("Lancement de la génération HTML.")
            build_html(feeds, entries)
            log.info("Site mis à jour avec succès.")
        else:
            log.error("Échec de la récupération des données réseau. Mise à jour ignorée.")

        log.debug(f"Mise en veille pour {UPDATE_TIME} secondes.")
        time.sleep(UPDATE_TIME)

if __name__ == "__main__":
    # Création du dossier web s'il n'existe pas
    os.makedirs(WEB_DIR, exist_ok=True)

    # Lancement du serveur web en arrière-plan
    # daemon=True : le serveur s'arrêtera proprement si le pod Kubernetes est détruit 
    threading.Thread(target=web_server, daemon=True).start()

    orchestrator()