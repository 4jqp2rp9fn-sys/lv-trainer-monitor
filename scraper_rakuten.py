"""
Rakuten Ichiba (楽天市場) search scraper.

Search results URL pattern:
    https://search.rakuten.co.jp/search/mall/<keyword>/

If Rakuten changes its HTML, update SELECTORS below. The scraper tries
multiple known card containers to stay resilient.
"""
import logging
from typing import Dict, List, Set
from urllib.parse import quote
from bs4 import BeautifulSoup

from utils import fetch, normalized_item, polite_sleep

log = logging.getLogger("rakuten")

SITE_NAME = "Rakuten"
BASE_SEARCH = "https://search.rakuten.co.jp/search/mall/{kw}/"

# --- Update these if HTML changes ---
SELECTORS = {
    # Any of these containers will be treated as a product card
    "card_candidates": [
        "div.searchresultitem",
        "div[class*='searchresultitem']",
        "div.dui-card.searchresultitem",
    ],
    "title_anchor": "h2 a, .title a, a.title-link, a[href*='item.rakuten.co.jp']",
    "price": "span.important, .price--OX_YW, [class*='price']",
}


def _build_url(keyword: str) -> str:
    return BASE_SEARCH.format(kw=quote(keyword))


def _parse(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    cards = []
    for sel in SELECTORS["card_candidates"]:
        cards = soup.select(sel)
        if cards:
            break
    if not cards:
        log.warning("No Rakuten cards matched any selector.")
        return []

    items: List[Dict] = []
    for card in cards:
        a = card.select_one(SELECTORS["title_anchor"])
        if not a:
            continue
        url = a.get("href", "").split("?")[0]
        title = a.get_text(strip=True)
        price_el = card.select_one(SELECTORS["price"])
        price = price_el.get_text(" ", strip=True) if price_el else ""

        if url and "item.rakuten.co.jp" in url:
            items.append(normalized_item(SITE_NAME, title, price, url))
    return items


def search(session, keywords: List[str]) -> List[Dict]:
    """Run all keyword searches and return de-duplicated normalized items."""
    seen_urls: Set[str] = set()
    out: List[Dict] = []
    for kw in keywords:
        url = _build_url(kw)
        log.info("Fetching Rakuten: %s", url)
        html = fetch(session, url)
        if not html:
            continue
        for item in _parse(html):
            if item["url"] in seen_urls:
                continue
            seen_urls.add(item["url"])
            out.append(item)
        polite_sleep(1.0)
    log.info("Rakuten: %d items collected.", len(out))
    return out
