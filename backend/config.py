import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Paths
DATA_DIR = BASE_DIR / "backend" / "data"
FRONTEND_DIR = BASE_DIR / "frontend"
DB_PATH = DATA_DIR / "trialsofjudah.db"
DATA_DIR.mkdir(exist_ok=True)

# Server
SERVER_HOST = os.getenv("HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", "8202"))

# LLM
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mixtral")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
