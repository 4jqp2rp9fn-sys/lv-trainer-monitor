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
    # sneakers
    "LV Trainer FD 0252",
    "Louis Vuitton trainer FD 0252",
    "ヴィトン トレーナー FD 0252",
    "ヴィトン トレイナー FD 0252",
    "chanel ハイカット",
    "chanel g32222",
    "cros bae taupe",
    "crocs ベイ トープ"


    # tops
    "Alexander Digenova",
    "rue porter パーカー",
    "vetements tonal logo hoodie",
    "Polo Ralph Lauren ループバック フルジップ フーティ MNPOKNI16824976001",
    "ポロ ラルフ ローレン ループバック フルジップ フーティ MNPOKNI16824976001"

    # pants
    "courreges 123DPA052DE00167011",
    "gosha adidas スウェットパンツ",
    "gosha adidas G013P103",
    "balenciaga 720511",
    "BALENCIAGA 675244"    

]

# --- Behavior ---
# On the very first run with an empty store, mark all current items as "seen"
# instead of spamming the webhook with the entire backlog.
SEED_ON_FIRST_RUN = os.getenv("SEED_ON_FIRST_RUN", "true").lower() == "true"
