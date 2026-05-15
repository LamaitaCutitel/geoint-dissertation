import os
from pathlib import Path
from dotenv import load_dotenv

# Director principal proiect
BASE_DIR = Path(__file__).resolve().parent.parent

# Calea exactă către .env
ENV_PATH = BASE_DIR / ".env"

# Încarcă explicit fișierul
load_dotenv(dotenv_path=ENV_PATH)

# API KEY Planet
PL_API_KEY = os.getenv("PL_API_KEY")

# Config GEOINT
AREA_NAME = "Galati, Romania"

BBOX_GALATI = [
    27.5,
    45.2,
    28.3,
    45.9
]

CRS_WGS84 = "EPSG:4326"

DATA_RAW = "data/raw"
DATA_PROCESSED = "data/processed"
DATA_OUTPUT = "data/output"