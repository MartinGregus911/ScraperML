# config.py

from pathlib import Path

# Root directory of the project (where this config.py lives)
ROOT = Path(__file__).resolve().parent

# Data directories
DATA_DIR = ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DEBUG_DIR = DATA_DIR / "debug"
LOG_DIR = DATA_DIR / "logs"

# Create folders if they don't exist
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, DEBUG_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)
