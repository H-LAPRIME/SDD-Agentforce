import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "").strip()

# ── Paramètres du modèle ─────────────────────────────────────────────────────
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen/qwen3.5-122b-a10b")
DEFAULT_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
USE_OLLAMA = os.getenv("LLM_PROVIDER", "ollama" if not NVIDIA_API_KEY else "nvidia").strip().lower() == "ollama"
RUN_PROFILE = os.getenv("AGENTFORGE_PROFILE", os.getenv("RUN_PROFILE", "fast")).strip().lower()
if RUN_PROFILE not in {"fast", "quality", "full"}:
    RUN_PROFILE = "fast"

if USE_OLLAMA:
    MODEL_CONFIG = {
        "provider": "ollama",
        "model": DEFAULT_MODEL,
        "api_key": "ollama",
        "base_url": DEFAULT_BASE_URL,
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 16384,
        "seed": 42,
        "team": False,  
    }
else:
    MODEL_CONFIG = {
        "provider": "nvidia",
        "model": os.getenv("MODEL_NAME", "qwen/qwen3.5-122b-a10b"),
        "api_key": NVIDIA_API_KEY,
        "base_url": "https://integrate.api.nvidia.com/v1",
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 16384,
        "seed": 42,
        "team": False,
    }

MODEL_ROLES = ("router", "team", "worker")

# ── Base URL NVIDIA NIM (OpenAI-compatible) ──────────────────────────────────
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
# ── Répertoire de sortie (projet généré) ─────────────────────────────────────
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output")).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Extraction Dynamique d'Environnement ─────────────────────────────────────
def get_mcp_config() -> dict:
    """
    Retourne la configuration MCP en fusionnant les variables d'environnement locales
    avec celles extraites dynamiquement depuis le prompt de l'utilisateur.
    """
    # Configuration de base (fallback)
    config = {
        "you_api_key": os.getenv("YDC_API_KEY", "ydc-sk-d2ecf95ea06df139-sUHLCyflf1LWlsGL4oOCHd9q56eAuCaX-3bb629dc"),
        "gith": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", ""),
        "database_url":  os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/agentforge"),
        "mongodb_uri":   os.getenv("MONGODB_URI",  "mongodb://localhost:27017"),
        "redis_url":     os.getenv("REDIS_URL",    "redis://localhost:6379"),
        "mysql_host":    os.getenv("MYSQL_HOST", "localhost"),
        "mysql_port":    os.getenv("MYSQL_PORT", "3306"),
        "mysql_user":    os.getenv("MYSQL_USER", "root"),
        "mysql_password": os.getenv("MYSQL_PASSWORD", ""),
        "mysql_database": os.getenv("MYSQL_DATABASE", ""),
        "output_dir": str(OUTPUT_DIR),
        "sqlite_db":  os.getenv("SQLITE_DB_PATH", str(OUTPUT_DIR / "dev.db")),
        "git_repo":   os.getenv("GIT_REPO_PATH",  str(OUTPUT_DIR)),
        "brave_api_key": os.getenv("BRAVE_API_KEY", ""),
        "supabase_url": os.getenv("SUPABASE_URL", ""),
        "supabase_service_key": os.getenv("SUPABASE_SERVICE_KEY", ""),
        "stripe_api_key": os.getenv("STRIPE_API_KEY", ""),
        "figma_access_token": os.getenv("FIGMA_ACCESS_TOKEN", ""),
        "resend_api_key": os.getenv("RESEND_API_KEY", ""),
        "cloudflare_api_token": os.getenv("CLOUDFLARE_API_TOKEN", ""),
        "cloudflare_account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID", ""),
        "analytics_provider": os.getenv("ANALYTICS_PROVIDER", "plausible"),
        "analytics_api_key": os.getenv("ANALYTICS_API_KEY", ""),
    }

    # Charger les variables extraites dynamiquement (si elles existent)
    extracted_env_path = Path("specs/extracted_env.yaml")
    if extracted_env_path.exists():
        try:
            with open(extracted_env_path, "r", encoding="utf-8") as f:
                extracted = yaml.safe_load(f)
                if isinstance(extracted, dict):
                    # Mettre à jour la config avec les valeurs extraites (priorité haute)
                    for key, value in extracted.items():
                        if value:
                            config[key] = str(value)
        except Exception as e:
            print(f"Erreur lors du chargement de {extracted_env_path}: {e}")

    return config
