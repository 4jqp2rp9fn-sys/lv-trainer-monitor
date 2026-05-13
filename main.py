"""
Entry point — polls Rakuten and 2nd STREET on a fixed interval and
notifies Discord about new listings matching the configured keywords.
"""
import logging
import time
from typing import Dict, List

import scraper_rakuten
import scraper_2ndstreet
from config import (
    KEYWORDS,
    POLL_INTERVAL_SECONDS,
    SEED_ON_FIRST_RUN,
    STORAGE_PATH,
)
from notifier import send_item
from storage import SeenStore
from utils import build_session, polite_sleep, setup_logging

log = logging.getLogger("main")

SCRAPERS = [
    ("Rakuten", scraper_rakuten.search),
    #("2nd STREET", scraper_2ndstreet.search),
]


def collect_all(session) -> List[Dict]:
    items: List[Dict] = []
    for name, fn in SCRAPERS:
        try:
            items.extend(fn(session, KEYWORDS))
        except Exception:
            log.exception("Scraper '%s' failed.", name)
    return items


def run_once(session, store: SeenStore) -> None:
    items = collect_all(session)
    if not items:
        log.info("No items returned this cycle.")
        return

    new_items = [it for it in items if it.get("url") and not store.has(it["url"])]
    log.info("Found %d new items (of %d total).", len(new_items), len(items))

    if store.is_empty() and SEED_ON_FIRST_RUN:
        log.info("First run: seeding store with %d URLs (no notifications).", len(new_items))
        store.add_many(it["url"] for it in new_items)
        return

    for it in new_items:
        if send_item(it):
            store.add_many([it["url"]])
            log.info("Notified: [%s] %s", it["site"], it["title"][:80])
        else:
            log.warning("Notification failed; will retry next cycle: %s", it["url"])
        polite_sleep(0.8)


def main() -> None:
    setup_logging()
    log.info("Sneaker monitor starting. Interval=%ss, keywords=%s",
             POLL_INTERVAL_SECONDS, KEYWORDS)
    session = build_session()
    store = SeenStore(STORAGE_PATH)

    run_once(session, store)

if __name__ == "__main__":
    main()
