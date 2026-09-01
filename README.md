# Développement - LoutikDIGEST

![Bannière LoutikDIGEST](https://raw.githubusercontent.com/loutik/design-assets/main/loutikdigest/banniere_loutikdigest.png)

## Contexte

LoutikDIGEST est un agrégateur de veille technologique conçu pour centraliser les flux RSS et les dernières publications issues d’une instance Miniflux, puis les présenter dans une page HTML statique rapide à consulter et facile à héberger. L’objectif du projet est de maintenir une vue synthétique des sources de veille, des actualités et des contenus pertinents pour l’infrastructure, les réseaux et le développement.

Le service interroge régulièrement le backend Miniflux, reconstruit le rendu HTML et sert le site localement via un petit serveur web intégré. Il est pensé pour une utilisation simple, automatisée et robuste en environnement conteneurisé.

---

## Structure du dépôt

L’organisation du dépôt suit la logique suivante :

```text
.
├── app/
│   ├── builder.py
│   ├── grabber.py
│   ├── logger.py
│   ├── main.py
│   ├── templates/
│   │   └── index.html
│   └── var/
│       └── html/
├── docs/
│   └── loutik-digest-diagramme-logique.excalidraw
├── DIGEST-ABOUT.md
├── Dockerfile
├── docker-compose.yaml
├── LICENSE.md
├── README.md
├── requirements.txt
└── .env.example
```

- **`app/`** : code applicatif du service de génération et de diffusion du digest.
- **`app/main.py`** : point d’entrée, orchestration du rafraîchissement et lancement du serveur web.
- **`app/grabber.py`** : récupération des flux et des articles depuis l’API Miniflux.
- **`app/builder.py`** : génération du fichier HTML final à partir du template Jinja2.
- **`app/templates/index.html`** : structure HTML et styles du site affiché.
- **`app/var/html/`** : répertoire cible contenant le site généré.
- **`docker-compose.yaml`** : configuration de lancement local du service containerisé.
- **`Dockerfile`** : image Python de runtime utilisée pour exécuter l’application.
- **`requirements.txt`** : dépendances Python du projet.
- **`docs/`** : fichiers de documentation et schémas associés au projet.

---

## Utilisation de LoutikDIGEST

### 1. Cloner le dépôt localement

```bash
git clone https://github.com/loutik/digest.git
cd digest
```

### 2. Préparer le fichier d’environnement

Le projet fournit un fichier modèle `.env.example`. Pour démarrer rapidement, copiez-le vers `.env` :

```bash
cp .env.example .env
```

Le fichier `.env` contient déjà les variables utiles pour le fonctionnement du service :

| Variable | Rôle | Valeur par défaut / exemple |
| --- | --- | --- |
| `UPDATE_TIME` | Fréquence de rafraîchissement du digest en secondes. | `300` dans le fichier d’exemple, `120` dans le code si non défini. |
| `MINIFLUX_DOMAIN` | Domaine de l’instance Miniflux à interroger. | `"miniflux.exemple"` |
| `MINIFLUX_TOKEN` | Jeton API utilisé pour authentifier les appels Miniflux. | `"token-api-miniflux"` |
| `DEBUG_MODE` | Niveau de journalisation de l’application. | `"INFO"` |
| `TIMEZONE` | Fuseau horaire utilisé pour l’affichage des dates et heures. | `"Europe/Paris"`, sinon `UTC` par défaut dans le code. |

> Les variables `MINIFLUX_DOMAIN` et `MINIFLUX_TOKEN` doivent rester hors du dépôt et ne pas être versionnées. Les autres valeurs peuvent être ajustées selon l’environnement de déploiement.

### 3. Lancer le projet en développement local

Le fichier `docker-compose.yaml` présent dans ce dépôt est prévu pour le développement local. Il sert le service sur le port `8000` avec les variables du fichier `.env`.

```bash
docker compose up --build
```

Pour arrêter le service :

```bash
docker compose down
```

### 4. Vérifier le service

```bash
curl http://localhost:8000
```

## Utiliser LoutikDIGEST en production

Pour un usage standard en environnement de production, il est possible de déployer l’application via Docker en tirant l’image publiée depuis le registre GitHub Container Registry (GHCR). L’image est nommée `ghcr.io/loutik/digest:latest`.

Exemple de fichier `docker-compose.yaml` :

```yaml
services:
  digest:
    image: ghcr.io/loutik/digest:latest
    container_name: loutik-digest
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
```

Le fichier `.env` doit alors contenir les valeurs de configuration applicative, notamment :

```env
MINIFLUX_DOMAIN="miniflux.exemple"
MINIFLUX_TOKEN="token-api-miniflux"
PORT=8000
UPDATE_TIME=300
DEBUG_MODE="INFO"
TIMEZONE="Europe/Paris"
```

Ce mode de déploiement est adapté à un usage classique, tandis que le `docker-compose.yaml` présent dans ce dépôt reste orienté développement local.

---

## Bonnes pratiques

1. **Stocker les secrets dans `.env`** : conserver les identifiants Miniflux et la configuration locale hors du dépôt.
2. **Adapter la fréquence de refresh** : régler `UPDATE_TIME` selon le volume attendu de données et la charge de l’API Miniflux.
3. **Surveiller les logs** : utiliser `DEBUG_MODE` pour diagnostiquer les erreurs de collecte, génération HTML ou exposition du service.
4. **Distinguer dev local et runtime standard** : garder le `docker-compose.yaml` pour le développement local et préférer un lancement manuel ou un orchestrateur pour une utilisation plus classique.

```bash
docker compose logs -f digest
```

---

## 👨‍💻 Mainteneurs

- **Louis MEDO** | [LinkedIn](https://www.linkedin.com/in/louismedo/) | [Portfolio](https://louis.loutik.fr/) | [GitHub](https://github.com/FireToak) | [louis.medo@loutik.fr](mailto:louis.medo@loutik.fr)

---

<div align="center">
<br>
<small><i>Dernière mise à jour : 31 août 2026</i></small>
</div>
