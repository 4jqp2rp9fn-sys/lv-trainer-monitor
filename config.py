"""
Centralized configuration for the sneaker monitor.

Edit KEYWORDS to change what is searched.
Edit SELECTORS_* dicts in each scraper module if site HTML changes.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Discord ---
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

# --- Polling ---
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))  # 5 min

# --- HTTP ---
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
)

# --- Storage ---
# On Render, mount a persistent disk and point STORAGE_PATH at it
# (e.g. /var/data/seen.json). Defaults to local file.
STORAGE_PATH = os.getenv("STORAGE_PATH", "seen.json")

# --- Search keywords (easy to extend) ---
KEYWORDS = [
    "LV Trainer",
    "Louis Vuitton trainer",
    "ヴィトン トレーナー",
    "ヴィトン トレイナー",
    "Alexander Digenova",
    "chanel ハイカット",
    "chanel g32222",
    "balenciaga 720511",
    "courreges 123DPA052DE00167011",
    "BALENCIAGA 675244",
    "gosha adidas スウェットパンツ",
    "gosha adidas G013P103",
    "rue porter パーカー"

]

# --- Behavior ---
# On the very first run with an empty store, mark all current items as "seen"
# instead of spamming the webhook with the entire backlog.
SEED_ON_FIRST_RUN = os.getenv("SEED_ON_FIRST_RUN", "true").lower() == "true"
