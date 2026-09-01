import logging
import sys
import os

LOG_LEVEL_STR = os.getenv("DEBUG_MODE", "INFO").upper()

numeric_level = getattr(logging, LOG_LEVEL_STR, logging.INFO)

logging.basicConfig(
    level=numeric_level,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

log = logging.getLogger("digest_app")