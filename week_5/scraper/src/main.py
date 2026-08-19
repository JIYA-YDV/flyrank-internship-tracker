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


def discover_book_urls() -> tuple[list[str], int, dict[str, str]]:
    """
    Crawl up to MAX_PAGES catalogue pages.
    Returns (unique_book_urls, catalogue_page_count, source_page_map).
    source_page_map: {book_url -> catalogue_page_url}
    """
    book_urls: list[str] = []
    seen: set[str] = set()
    source_page_map: dict[str, str] = {}
    current_url: str | None = START_URL
    page_count = 0

    while current_url and page_count < MAX_PAGES:
        html, _ = fetch(current_url)
        page_count += 1
        this_page = current_url         # capture for closure

        for url in get_book_urls_from_page(html, this_page):
            if url not in seen:
                seen.add(url)
                book_urls.append(url)
                source_page_map[url] = this_page

        current_url = get_next_page_url(html, this_page)

    log.info(
        "catalogue_pages=%d  discovered=%d  unique_urls=%d",
        page_count, len(book_urls), len(set(book_urls)),
    )
    return book_urls, page_count, source_page_map
    
    if __name__ == "__main__":
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    urls, n_pages, src_map = discover_book_urls()
    raw_records, failed = scrape_all_books(urls, src_map)

    print(f"\ndetail_pages={len(raw_records)}")
    print(json.dumps(raw_records[0], indent=2))
    
# ── Stage 3: raw extraction ───────────────────────────────────────────────────

def extract_raw_record(
    html: str,
    product_url: str,
    source_page: str,
    fetched_at: str,
) -> dict:
    """
    Parse one book-detail page into a raw record.
    All values are strings (or None); cleaning happens in Stage 4.
    """
    soup = BeautifulSoup(html, "html.parser")

    # ── Title ─────────────────────────────────────────────────────────────────
    title_tag = soup.select_one("div.product_main > h1")
    title = title_tag.get_text(strip=True) if title_tag else None

    # ── Price ─────────────────────────────────────────────────────────────────
    price_tag = soup.select_one("div.product_main > p.price_color")
    price_text = price_tag.get_text(strip=True) if price_tag else None

    # ── Availability ──────────────────────────────────────────────────────────
    avail_tag = soup.select_one("div.product_main > p.availability")
    availability_text = avail_tag.get_text(strip=True) if avail_tag else None

    # ── Star rating (word form, e.g. "Three") ────────────────────────────────
    rating_tag = soup.select_one("div.product_main > p.star-rating")
    rating_text = rating_tag["class"][1] if rating_tag else None   # second CSS class

    # ── Description (optional — null when absent) ─────────────────────────────
    desc_header = soup.find("div", id="product_description")
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        description = desc_p.get_text(strip=True) if desc_p else None
    else:
        description = None          # not invented — genuinely absent

    return {
        "title":             title,
        "product_url":       product_url,
        "price_text":        price_text,
        "availability_text": availability_text,
        "rating_text":       rating_text,
        "description":       description,
        "source_page":       source_page,
        "fetched_at":        fetched_at,
    }


def scrape_book(url: str, source_page: str) -> dict | None:
    """
    Fetch (or cache) one book page and return its raw record.
    Returns None on any fetch failure.
    """
    try:
        html, _ = fetch(url)
    except RuntimeError as exc:
        log.warning("FAILED     %s  →  %s", url, exc)
        return None

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return extract_raw_record(html, url, source_page, fetched_at)


def scrape_all_books(
    book_urls: list[str],
    source_page_map: dict[str, str],
) -> tuple[list[dict], list[str]]:
    """
    Visit every book URL.
    Returns (raw_records, failed_urls).
    """
    raw_records: list[dict] = []
    failed_urls: list[str] = []

    for url in book_urls:
        record = scrape_book(url, source_page_map.get(url, "unknown"))
        if record is None:
            failed_urls.append(url)
        else:
            raw_records.append(record)

    log.info(
        "detail_pages=%d  failed=%d",
        len(raw_records), len(failed_urls),
    )
    return raw_records, failed_urls

    
if __name__ == "__main__":
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    urls, n_pages = discover_book_urls()
    print(f"\ncatalogue_pages={n_pages}  unique_urls={len(urls)}\n")
    # Expected: catalogue_pages=3  unique_urls=60