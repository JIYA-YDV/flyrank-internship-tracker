"""
A9 — The Polite Scraper
Books to Scrape · Python lane · FlyRank Internship Week 5
"""

import json
import re
import time
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, field_validator

# ── Configuration ─────────────────────────────────────────────────────────────

BASE_URL   = "https://books.toscrape.com/catalogue/"
START_URL  = "https://books.toscrape.com/catalogue/page-1.html"
REPO_URL   = "https://github.com/YOUR_USERNAME/YOUR_REPO"
USER_AGENT = f"FlyRankInternshipA9/1.0 (+{REPO_URL})"

TIMEOUT_SECONDS = 10
DELAY_SECONDS   = 0.5
MAX_PAGES       = 3

CACHE_DIR  = Path("cache")
OUTPUT_DIR = Path("output")

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("scraper")

# ── Schema ────────────────────────────────────────────────────────────────────

class BookRecord(BaseModel):
    title:             str
    product_url:       str
    price_text:        str
    price_gbp:         float
    availability_text: str
    rating_text:       str
    description:       Optional[str] = None
    source_page:       str
    fetched_at:        str

    @field_validator("product_url", "source_page")
    @classmethod
    def must_be_https(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError(f"URL must start with https:// — got: {v!r}")
        return v

    @field_validator("price_gbp")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"price_gbp must be positive, got {v}")
        return v

# ── Cache helpers ─────────────────────────────────────────────────────────────

def _cache_key(url: str) -> Path:
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    slug   = urlparse(url).path.strip("/").replace("/", "_")[-40:]
    return CACHE_DIR / f"{slug}_{digest}.html"

# ── Fetch ─────────────────────────────────────────────────────────────────────

def fetch(url: str) -> tuple[str, bool]:
    """Return (html, from_cache). Raises RuntimeError on non-200."""
    cache_file = _cache_key(url)

    if cache_file.exists():
        log.info("CACHE HIT  %s", url)
        return cache_file.read_text(encoding="utf-8"), True

    time.sleep(DELAY_SECONDS)
    log.info("FETCH      %s", url)

    resp = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT_SECONDS,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code} for {url}")

    html = resp.text
    cache_file.write_text(html, encoding="utf-8")
    log.info("SAVED      %s  (%d bytes)", cache_file.name, len(html))
    return html, False

# ── Discovery ─────────────────────────────────────────────────────────────────

def get_book_urls_from_page(html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for article in soup.select("article.product_pod"):
        a_tag = article.select_one("h3 > a")
        if a_tag and a_tag.get("href"):
            urls.append(urljoin(page_url, a_tag["href"]))
    return urls

def get_next_page_url(html: str, current_url: str) -> str | None:
    soup     = BeautifulSoup(html, "html.parser")
    next_btn = soup.select_one("li.next > a")
    if next_btn and next_btn.get("href"):
        return urljoin(current_url, next_btn["href"])
    return None

def discover_book_urls() -> tuple[list[str], int, dict[str, str]]:
    book_urls: list[str]       = []
    seen: set[str]             = set()
    source_page_map            = {}
    current_url: str | None    = START_URL
    page_count                 = 0

    while current_url and page_count < MAX_PAGES:
        html, _ = fetch(current_url)
        page_count += 1
        this_page = current_url

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

# ── Extraction ────────────────────────────────────────────────────────────────

def extract_raw_record(
    html: str,
    product_url: str,
    source_page: str,
    fetched_at: str,
) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title_tag    = soup.select_one("div.product_main > h1")
    price_tag    = soup.select_one("div.product_main > p.price_color")
    avail_tag    = soup.select_one("div.product_main > p.availability")
    rating_tag   = soup.select_one("div.product_main > p.star-rating")
    desc_header  = soup.find("div", id="product_description")

    description = None
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        description = desc_p.get_text(strip=True) if desc_p else None

    return {
        "title":             title_tag.get_text(strip=True) if title_tag else None,
        "product_url":       product_url,
        "price_text":        price_tag.get_text(strip=True) if price_tag else None,
        "availability_text": avail_tag.get_text(strip=True) if avail_tag else None,
        "rating_text":       rating_tag["class"][1] if rating_tag else None,
        "description":       description,
        "source_page":       source_page,
        "fetched_at":        fetched_at,
    }

# ── Scrape one book (with retry) ──────────────────────────────────────────────

def scrape_book(url: str, source_page: str) -> dict | None:
    for attempt in (1, 2):
        try:
            html, _ = fetch(url)
            fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            return extract_raw_record(html, url, source_page, fetched_at)

        except requests.exceptions.Timeout:
            log.warning("TIMEOUT    %s  (attempt %d/2)", url, attempt)
            if attempt == 1:
                time.sleep(2)

        except RuntimeError as exc:
            msg = str(exc)
            if "404" in msg or "403" in msg:
                log.warning("PERMANENT  %s  →  %s", url, msg)
                return None
            log.warning("SERVER ERR %s  →  %s  (attempt %d/2)", url, msg, attempt)
            if attempt == 1:
                time.sleep(2)

        except Exception as exc:
            log.warning("FAILED     %s  →  %s", url, exc)
            return None

    log.error("GIVING UP  %s", url)
    return None

# ── Normalization & validation ────────────────────────────────────────────────

def parse_price(price_text: str) -> float:
    digits = re.sub(r"[^\d.]", "", price_text)
    return float(digits)

def normalize(raw: dict) -> dict:
    return {**raw, "price_gbp": parse_price(raw["price_text"])}

def validate_records(raw_records: list[dict]) -> tuple[list[BookRecord], list[dict]]:
    good:   list[BookRecord] = []
    errors: list[dict]       = []
    seen:   set[str]         = set()

    for raw in raw_records:
        url = raw.get("product_url", "")
        if url in seen:
            continue
        seen.add(url)

        try:
            record = BookRecord(**normalize(raw))
            good.append(record)
        except Exception as exc:
            errors.append({**raw, "error": str(exc)})
            log.warning("INVALID    %s  →  %s", url, exc)

    log.info("valid=%d  invalid=%d", len(good), len(errors))
    return good, errors

# ── Save JSON ─────────────────────────────────────────────────────────────────

def save_json(data: list, path: Path) -> None:
    payload = [r.model_dump() if isinstance(r, BookRecord) else r for r in data]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("SAVED      %s  (%d records)", path, len(payload))

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    CACHE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    run_start = datetime.now(timezone.utc)

    urls, n_pages, src_map = discover_book_urls()

    # Inject one deliberately broken URL to prove graceful failure
    FAKE_URL = "https://books.toscrape.com/catalogue/does-not-exist_9999/index.html"
    if FAKE_URL not in urls:
        urls.append(FAKE_URL)
        src_map[FAKE_URL] = "injected-for-testing"

    raw_records: list[dict] = []
    failed_urls: list[str]  = []
    cache_hits = 0

    for url in urls:
        was_cached = _cache_key(url).exists()
        record     = scrape_book(url, src_map.get(url, "unknown"))
        if was_cached:
            cache_hits += 1
        if record is None:
            failed_urls.append(url)
        else:
            raw_records.append(record)

    log.info(
        "detail_pages=%d  failed=%d",
        len(raw_records), len(failed_urls),
    )

    good, errors = validate_records(raw_records)
    save_json(good,   OUTPUT_DIR / "books.json")
    save_json(errors, OUTPUT_DIR / "errors.json")

    run_end = datetime.now(timezone.utc)
    run_report = {
        "started_at":           run_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "finished_at":          run_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "duration_seconds":     round((run_end - run_start).total_seconds(), 1),
        "catalogue_pages":      n_pages,
        "discovered_urls":      len(urls),
        "detail_pages_fetched": len(raw_records) + len(failed_urls),
        "cache_hits":           cache_hits,
        "valid_records":        len(good),
        "invalid_records":      len(errors),
        "failed_pages":         len(failed_urls),
        "failed_urls":          failed_urls,
    }

    report_path = OUTPUT_DIR / "run-report.json"
    report_path.write_text(json.dumps(run_report, indent=2), encoding="utf-8")

    print("\n── Run complete ──────────────────────────────────────")
    print(f"  Catalogue pages  : {run_report['catalogue_pages']}")
    print(f"  Discovered URLs  : {run_report['discovered_urls']}")
    print(f"  Valid records    : {run_report['valid_records']}")
    print(f"  Invalid records  : {run_report['invalid_records']}")
    print(f"  Failed pages     : {run_report['failed_pages']}")
    print(f"  Cache hits       : {run_report['cache_hits']}")
    print(f"  Duration         : {run_report['duration_seconds']}s")
    print("──────────────────────────────────────────────────────\n")