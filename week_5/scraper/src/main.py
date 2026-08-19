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
    
    
# ── Stage 2: catalogue crawler ────────────────────────────────────────────────

def get_book_urls_from_page(html: str, page_url: str) -> list[str]:
    """Extract absolute book-detail URLs from one catalogue page."""
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for article in soup.select("article.product_pod"):
        a_tag = article.select_one("h3 > a")
        if a_tag and a_tag.get("href"):
            absolute = urljoin(page_url, a_tag["href"])
            urls.append(absolute)
    return urls


def get_next_page_url(html: str, current_url: str) -> str | None:
    """Follow the catalogue's own 'next' link — never hardcode page numbers."""
    soup = BeautifulSoup(html, "html.parser")
    next_btn = soup.select_one("li.next > a")
    if next_btn and next_btn.get("href"):
        return urljoin(current_url, next_btn["href"])
    return None


def discover_book_urls() -> tuple[list[str], int]:
    """
    Crawl up to MAX_PAGES catalogue pages.
    Returns (unique_book_urls, catalogue_page_count).
    """
    book_urls: list[str] = []
    seen: set[str] = set()
    current_url: str | None = START_URL
    page_count = 0

    while current_url and page_count < MAX_PAGES:
        html, _ = fetch(current_url)
        page_count += 1

        for url in get_book_urls_from_page(html, current_url):
            if url not in seen:
                seen.add(url)
                book_urls.append(url)

        current_url = get_next_page_url(html, current_url)

    log.info(
        "catalogue_pages=%d  discovered=%d  unique_urls=%d",
        page_count, len(book_urls), len(set(book_urls)),
    )
    return book_urls, page_count
    
    
if __name__ == "__main__":
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    urls, n_pages = discover_book_urls()
    print(f"\ncatalogue_pages={n_pages}  unique_urls={len(urls)}\n")
    # Expected: catalogue_pages=3  unique_urls=60