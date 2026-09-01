import os
from jinja2 import Environment, FileSystemLoader
# Modules internes
from logger import log
from datetime import datetime
from zoneinfo import ZoneInfo

# Variables

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "templates")
HTML_OUTPUT = os.path.join(SCRIPT_DIR, "var", "html", "index.html")
templateFolder = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
timezone = ZoneInfo(os.getenv("TIMEZONE", "UTC"))
APP_VERSION = os.environ.get("APP_VERSION", "N/A")

# Logique

def build_html(feeds_data, entries_data):
    log.debug("Initialisation de Jinja2 (moteur de template).")

    now = datetime.now(timezone)
    DATE = now.strftime('%d-%m-%Y')
    HOUR = now.strftime('%H:%M:%S')
    
    log.debug("Chargement du modèle index.html.")
    template = templateFolder.get_template("index.html")
    
    log.debug("Fusion des données Python avec le HTML.")
    html_result = template.render(feeds=feeds_data, entries=entries_data, DATE=DATE, HOUR=HOUR, APP_VERSION=APP_VERSION)

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"{html_result}")
    
    return html_result
