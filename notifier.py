"""Discord webhook notifier."""
import logging
import requests

from config import DISCORD_WEBHOOK_URL, REQUEST_TIMEOUT

log = logging.getLogger("notifier")


def _color_for(site: str) -> int:
    return {
        "Rakuten": 0xBF0000,
        "2nd STREET": 0x111111,
    }.get(site, 0x5865F2)


def send_item(item: dict) -> bool:
    """Send a single item to Discord. Returns True on success."""
    if not DISCORD_WEBHOOK_URL:
        log.error("DISCORD_WEBHOOK_URL not configured.")
        return False

    embed = {
        "title": item.get("title") or "(no title)",
        "url": item.get("url"),
        "color": _color_for(item.get("site", "")),
        "fields": [
            {"name": "Price", "value": item.get("price") or "—", "inline": True},
            {"name": "Site", "value": item.get("site") or "—", "inline": True},
        ],
    }
    payload = {"embeds": [embed]}

    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=REQUEST_TIMEOUT)
        if r.status_code in (200, 204):
            return True
        log.warning("Discord responded %s: %s", r.status_code, r.text[:200])
        return False
    except requests.RequestException as e:
        log.error("Discord webhook error: %s", e)
        return False
