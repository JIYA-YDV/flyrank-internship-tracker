"""
A9 — The Polite Scraper
Books to Scrape · Python lane
"""

import json
import time
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ── Configuration ────────────────────────────────────────────────────────────

BASE_URL   = "https://books.toscrape.com/catalogue/"
START_URL  = "https://books.toscrape.com/catalogue/page-1.html"
REPO_URL   = "https://github.com/YOUR_USERNAME/YOUR_REPO"   # ← change this
USER_AGENT = f"FlyRankInternshipA9/1.0 (+{REPO_URL})"

TIMEOUT_SECONDS  = 10
DELAY_SECONDS    = 0.5      # minimum wait between real requests
MAX_PAGES        = 3        # catalogue pages to crawl

CACHE_DIR  = Path("cache")
OUTPUT_DIR = Path("output")

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("scraper")


# ── Cache helpers ─────────────────────────────────────────────────────────────

def _cache_key(url: str) -> Path:
    """Deterministic filename: sha256 of the URL (safe on all OSes)."""
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    # also embed a human-readable slug from the URL path
    slug = urlparse(url).path.strip("/").replace("/", "_")[-40:]
    return CACHE_DIR / f"{slug}_{digest}.html"


def fetch(url: str) -> tuple[str, bool]:
    """
    Return (html_text, from_cache).

    Raises RuntimeError on non-200 status.
    Waits DELAY_SECONDS before every real network request.
    """
    cache_file = _cache_key(url)

    if cache_file.exists():
        log.info("CACHE HIT  %s  (%d bytes)", url, cache_file.stat().st_size)
        return cache_file.read_text(encoding="utf-8"), True

    # polite delay before every real request
    time.sleep(DELAY_SECONDS)

    log.info("FETCH      %s", url)
    resp = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT_SECONDS,
    )

    if resp.status_code != 200:
        raise RuntimeError(
            f"Non-200 status {resp.status_code} for {url}"
        )

    html = resp.text
    cache_file.write_text(html, encoding="utf-8")
    log.info("SAVED      %s  (%d bytes)", cache_file.name, len(html))
    return html, False
    
    
    # ── Stage 1 smoke test (remove after checkpoint) ──────────────────────────────
if __name__ == "__main__":
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    html, from_cache = fetch(START_URL)
    source = "CACHE HIT" if from_cache else "FETCH"
    print(f"\n{source}  |  size={len(html):,} bytes\n")