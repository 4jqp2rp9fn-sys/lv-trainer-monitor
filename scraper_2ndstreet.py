"""
2nd STREET Online Store scraper.

Search URL pattern:
    https://www.2ndstreet.jp/search?keyword=<keyword>

Update SELECTORS below if HTML structure changes.
"""
import logging
from typing import Dict, List, Set
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

from utils import fetch, normalized_item, polite_sleep

log = logging.getLogger("2ndstreet")

SITE_NAME = "2nd STREET"
BASE = "https://www.2ndstreet.jp"
BASE_SEARCH = BASE + "/search?keyword={kw}"

# --- Update these if HTML changes ---
SELECTORS = {
    "card_candidates": [
        "li.product-list-item",
        "div.product-list-item",
        "li[class*='product-list']",
        "div[class*='ProductCard']",
    ],
    "title": ".product-list-item-name, .product-name, [class*='Name']",
    "price": ".product-list-item-price, .price, [class*='Price']",
    "anchor": "a[href*='/goods/detail/']",
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
        log.warning("No 2nd STREET cards matched any selector.")
        return []

    items: List[Dict] = []
    for card in cards:
        a = card.select_one(SELECTORS["anchor"])
        if not a:
            continue
        href = a.get("href", "")
        url = urljoin(BASE, href).split("?")[0]

        title_el = card.select_one(SELECTORS["title"])
        title = title_el.get_text(" ", strip=True) if title_el else a.get_text(strip=True)

        price_el = card.select_one(SELECTORS["price"])
        price = price_el.get_text(" ", strip=True) if price_el else ""

        if url:
            items.append(normalized_item(SITE_NAME, title, price, url))
    return items


def search(session, keywords: List[str]) -> List[Dict]:
    seen_urls: Set[str] = set()
    out: List[Dict] = []
    for kw in keywords:
        url = _build_url(kw)
        log.info("Fetching 2nd STREET: %s", url)
        html = fetch(session, url)
        if not html:
            continue
        for item in _parse(html):
            if item["url"] in seen_urls:
                continue
            seen_urls.add(item["url"])
            out.append(item)
        polite_sleep(1.0)
    log.info("2nd STREET: %d items collected.", len(out))
    return out
