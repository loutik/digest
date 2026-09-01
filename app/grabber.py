import requests
# Modules internes
from logger import log

# Logique
def fetch_data(MINIFLUX_DOMAIN, MINIFLUX_TOKEN):
    log.debug(f"Début de la collecte sur : {MINIFLUX_DOMAIN}")
    headers = {"X-Auth-Token": MINIFLUX_TOKEN}

    try:
        log.debug("Envoi de la requête GET pour les sources.")
        res_feeds = requests.get(f"https://{MINIFLUX_DOMAIN}/v1/feeds", headers=headers, timeout=5)

        log.debug("Envoi de la requête GET pour les articles.")
        res_entries = requests.get(f"https://{MINIFLUX_DOMAIN}/v1/entries?limit=20&order=published_at&direction=desc", headers=headers, timeout=5)

        if res_feeds.status_code == 200 and res_entries.status_code == 200:
            log.debug("Lecture et renvoi des données.")
            
            feeds_data = res_feeds.json()
            entries_data = res_entries.json().get("entries", [])
            
            return feeds_data, entries_data
        else:
            log.error(f"Problème API Miniflux. Codes HTTP : {res_feeds.status_code} / {res_entries.status_code}")
            return None, None

    except requests.RequestException as e:
        log.error(f"Impossible de joindre le serveur : {e}")
        return None, None