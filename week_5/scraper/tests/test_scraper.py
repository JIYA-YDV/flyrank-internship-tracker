"""
Unit tests — Stage 6.
Run with:  python -m pytest tests/ -v
"""

import pytest
from src.main import (
    parse_price,
    normalize,
    BookRecord,
    get_book_urls_from_page,
    get_next_page_url,
    extract_raw_record,
)
from urllib.parse import urljoin


# ── 1. Price normalization ────────────────────────────────────────────────────

def test_parse_price_standard():
    assert parse_price("£51.77") == pytest.approx(51.77)

def test_parse_price_no_symbol():
    assert parse_price("12.99") == pytest.approx(12.99)

def test_parse_price_zero_raises():
    """A zero price should be caught by the Pydantic validator."""
    raw = _base_raw(price_text="£0.00")
    with pytest.raises(Exception, match="positive"):
        BookRecord(**normalize(raw))


# ── 2. Relative → absolute URL ────────────────────────────────────────────────

def test_relative_to_absolute():
    page_url = "https://books.toscrape.com/catalogue/page-1.html"
    href     = "../a-light-in-the-attic_1000/index.html"
    result   = urljoin(page_url, href)
    assert result.startswith("https://")
    assert "books.toscrape.com" in result


# ── 3. Missing description → None ────────────────────────────────────────────

def test_missing_description_is_null():
    html = """
    <html><body>
      <div class="product_main">
        <h1>No Desc Book</h1>
        <p class="price_color">£9.99</p>
        <p class="availability">In stock</p>
        <p class="star-rating Three"></p>
      </div>
    </body></html>
    """
    record = extract_raw_record(
        html,
        "https://books.toscrape.com/catalogue/no-desc/index.html",
        "https://books.toscrape.com/catalogue/page-1.html",
        "2025-01-01T00:00:00Z",
    )
    assert record["description"] is None


# ── 4. Duplicate URLs are de-duplicated ──────────────────────────────────────

def test_validate_deduplicates():
    from src.main import validate_records
    raw = _base_raw()
    good, errors = validate_records([raw, raw])   # same URL twice
    assert len(good) == 1
    assert len(errors) == 0


# ── 5. Malformed fixture (missing price) → lands in errors ───────────────────

def test_invalid_price_text_goes_to_errors():
    from src.main import validate_records
    raw = _base_raw(price_text="NOT_A_PRICE_XYZ")
    good, errors = validate_records([raw])
    # parse_price strips non-digits → empty string → float("") raises ValueError
    assert len(good) == 0
    assert len(errors) == 1
    assert "error" in errors[0]


# ── helpers ───────────────────────────────────────────────────────────────────

def _base_raw(**overrides) -> dict:
    base = {
        "title":             "Test Book",
        "product_url":       "https://books.toscrape.com/catalogue/test/index.html",
        "price_text":        "£12.34",
        "availability_text": "In stock",
        "rating_text":       "Three",
        "description":       "A test book.",
        "source_page":       "https://books.toscrape.com/catalogue/page-1.html",
        "fetched_at":        "2025-01-01T00:00:00Z",
    }
    base.update(overrides)
    return base