"""HTTP and logging utilities."""
import logging
from typing import Optional
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import USER_AGENT, REQUEST_TIMEOUT, MAX_RETRIES


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def build_session() -> requests.Session:
    """Session with sane defaults + retry policy."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def fetch(session: requests.Session, url: str) -> Optional[str]:
    """GET a URL and return response text or None on error."""
    log = logging.getLogger("fetch")
    try:
        r = session.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        if r.status_code != 200:
            log.warning("Non-200 (%s) for %s", r.status_code, url)
            return None
        return r.text
    except requests.RequestException as e:
        log.warning("Request failed for %s: %s", url, e)
        return None


def normalized_item(site: str, title: str, price: str, url: str) -> dict:
    return {
        "site": site,
        "title": (title or "").strip(),
        "price": (price or "").strip(),
        "url": (url or "").strip(),
    }


def polite_sleep(seconds: float = 1.0) -> None:
    time.sleep(seconds)
