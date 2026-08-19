# A9 — The Polite Scraper

A small, polite scraping pipeline that downloads the first three catalogue
pages of [Books to Scrape](https://books.toscrape.com), visits all 60 book
pages, turns messy HTML into clean, validated JSON records, survives broken
pages without crashing, and ends every run with an honest report.

**FlyRank Internship · Backend Track · Week 5 · Assignment A9**

---

## Target Classification

| Field          | Value                                                       |
|----------------|-------------------------------------------------------------|
| **Site**       | Books to Scrape — https://books.toscrape.com                |
| **Why chosen** | A public sandbox built explicitly for scraping practice     |
| **Scope**      | First 3 catalogue pages only (60 books)                     |
| **Data**       | Title, price, availability, rating, description, URLs       |
| **robots.txt** | File exists at `/robots.txt`; no `Disallow` rules found — all paths are allowed |

The [toscrape.com](https://toscrape.com) landing page explicitly states this
is a sandbox for web scraping practice. That statement is the permission for
this project.

> **"I will not reuse this code on another site without checking its rules
> and terms first."**

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip

### Install and Run (Windows PowerShell)

```powershell
# Clone the repo
git clone https://github.com/YOUR_USERNAME/flyrank-internship-tracker.git
cd flyrank-internship-tracker/week_5/scraper

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python src/main.py

# Run tests
python -m pytest tests/ -v
```
# Install and Run (macOS / Linux)

git clone [https://github.com/YOUR_USERNAME/flyrank-internship-tracker.git](https://github.com/JIYA-YDV/flyrank-internship-tracker/tree/main/week_5/scraper)

cd flyrank-internship-tracker/week_5/scraper

python -m venv venv && source venv/bin/activate

pip install -r requirements.txt

python src/main.py

python -m pytest tests/ -v

Total time from clone to output: ~2 minutes (first run fetches 63 pages with polite delays; re-runs finish in seconds from cache).

# Output Files

|File |	Description |
|-----|-------------|
|output/books.json | 60 validated, deduplicated book records |
|output/errors.json |	Records that failed schema validation |
|output/run-report.json	| Run statistics: counts, timing, failures |

# Record Schema

Every record in books.json follows this schema, enforced by Pydantic:

{

  "title":             "string (required)",
  
  "product_url":       "string, must start with https:// (required, unique identity)",
  
  "price_text":        "string, original text e.g. '£51.77' (required)",
  
  "price_gbp":         "float, parsed number e.g. 51.77, must be > 0 (required)",
  
  "availability_text": "string (required)",
  
  "rating_text":       "string, e.g. 'Three' (required)",
  
  "description":       "string or null (optional — null when the page has none)",
  
  "source_page":       "string, catalogue page URL (required)",
  
  "fetched_at":        "string, ISO-8601 UTC timestamp (required)"
  
}

#  Example record(My Output)

{

  "title": "The Natural History of Us (The Fine Art of Pretending #2)",
    
  "product_url": "https://books.toscrape.com/catalogue/the-natural-history-of-us-the-fine-art-of-pretending-2_941/index.html",
   
  "price_text": "Ã‚Â£45.22",
    
  "price_gbp": 45.22,
    
  "availability_text": "In stock (16 available)",
    
  "rating_text": "Three",
    
  "description": "One class assignment. One second chance at love. The school player is all in. Now he needs to win back the sweet commitment girl who's forever owned his heart. Justin Carter has a secret. He's not the total player Fairfield Academy believes him to be. Not really. In fact, he used to be a one-woman guy...and his feelings for her never went away. Too bad he broke her heart t One class assignment. One second chance at love. The school player is all in. Now he needs to win back the sweet commitment girl who's forever owned his heart. Justin Carter has a secret. He's not the total player Fairfield Academy believes him to be. Not really. In fact, he used to be a one-woman guy...and his feelings for her never went away. Too bad he broke her heart three years ago and made sure to ruin any chance she'd ever forgive him. Peyton Williams is a liar. She pretends to be whole, counting down the days until graduation and helping her parents at the family ranch. But the truth is, she's done everything she can to get over Justin, and salvation is just around the corner. With graduation one short month away, she'll soon break free from the painful memories and start her life fresh. Of course, she has to get through working with him on one last assignment first. For Justin, nothing ever felt as right as being with Peyton, and now that fate's given him a shot at redemption, he's determined to make the most of it. And for Peyton...well, Justin Carter has always been her kryptonite. ...more",
    
  "source_page": "https://books.toscrape.com/catalogue/page-3.html",
    
  "fetched_at": "2026-08-19T19:26:27Z"
  }

<img width="752" height="596" alt="image" src="https://github.com/user-attachments/assets/03fdc029-f067-4c8e-81c5-76445eafdd47" />

# Politeness Rules

This scraper follows professional courtesy rules:

| Rule | Implementation |
|------|----------------|
|User-Agent	| FlyRankInternshipA9/1.0 (+repo_url) — identifies who and why |
|Delay |	≥ 500ms between every real network request |
|Timeout |	10 seconds per request — never waits forever |
|Cache |	HTML saved to cache/; development reads cache, never re-fetches |
|Status | check	Only HTTP 200 is treated as success |
|Retry |	One retry on 5xx/timeout; no retry on 404 or 403 |
|Scope |	Only 3 catalogue pages — never crawls the full site |

# Error Handling 

- Each page is processed independently — one failure cannot crash the run

- 5xx errors and timeouts get one retry after a 2-second wait

- 404 and 403 are permanent failures — no retry (the page is gone or blocked)

- Failed pages are logged, skipped, and reported in run-report.json

- A deliberately injected fake URL proves this works every run

# Tests

7 unit tests covering core functionality:

tests/test_scraper.py::test_parse_price_standard              PASSED

tests/test_scraper.py::test_parse_price_no_symbol             PASSED

tests/test_scraper.py::test_parse_price_zero_raises           PASSED

tests/test_scraper.py::test_relative_to_absolute              PASSED

tests/test_scraper.py::test_missing_description_is_null       PASSED

tests/test_scraper.py::test_validate_deduplicates             PASSED

tests/test_scraper.py::test_invalid_price_text_goes_to_errors PASSED

<img width="737" height="350" alt="Screenshot 2026-08-20 005912" src="https://github.com/user-attachments/assets/46d607f2-9e72-4292-b4b3-80b68896391f" />

3 Run tests with:

PowerShell

python -m pytest tests/ -v

# Why No Browser Was Needed

All book data (title, price, availability, rating, description) is present in the server-rendered HTML that a plain HTTP request returns. No JavaScript executes to load this content. Using a browser (e.g., Playwright) would add ~200MB of dependencies and 10x the memory usage for zero additional data.

# Pipeline Architecture

classify → fetch → cache → discover → extract → normalize → validate → store → report

|Step	| What it does |
|-----|--------------|
| Classify |	Confirm target is a sandbox, check robots.txt |
| Fetch |	GET with user-agent, timeout, status check |
| Cache |	Save HTML locally; re-reads skip the network |
| Discover |	Follow catalogue "next" links, collect book URLs |
| Extract |	Parse HTML → 8 raw fields per book |
| Normalize |	"£51.77" → 51.77 (keep both) |
| Validate |	Pydantic schema check; failures → errors.json |
| Store |	Deduplicated records → books.json |
| Report |	Honest numbers → run-report.json |

# Project Structure

```
scraper/
├── src/
│   └── main.py              # The complete scraper
├── tests/
│   └── test_scraper.py      # 7 unit tests
├── output/
│   ├── books.json           # 60 validated records
│   ├── errors.json          # Validation failures
│   └── run-report.json      # Run statistics
├── cache/                   # HTML cache (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```
# Limitations 

- Only covers the first 3 catalogue pages (60 of ~1000 books)
  
- No JavaScript rendering — would miss JS-loaded content on other sites
  
- Single-threaded — processes pages sequentially
  
- Cache has no expiry — stale HTML must be manually deleted
  
# Ethics Note

- Use an official API whenever one exists — scraping is a last resort
  
- Never bypass logins, paywalls, CAPTCHAs, or access controls
  
- Collect only the data you actually need
  
- Always check a site's robots.txt and terms of service before scraping
  
- Identify yourself honestly via the User-Agent header
  
- Go slowly — a scraper should be the quietest visitor on a site
  
# Tech Stack 

| Tool |	Purpose |
|------|----------|
| Python 3.10+ |	Language |
| Requests |	HTTP client |
| Beautiful Soup 4 |	HTML parser |
| Pydantic |	Schema validation |
| pytest |	Unit testing |

## Full Command Sequence (PowerShell)

Run this whole block to finish everything:

```powershell
# 1. Go to your scraper folder
cd D:\flyrankai\flyrank-internship-tracker\week_5\scraper

# 2. Activate venv
.\venv\Scripts\Activate.ps1

# 3. Run the scraper to generate output files
python src/main.py

# 4. Confirm output files exist
ls output/

# 5. View the run report (copy this into README)
cat output/run-report.json

# 6. Save the new README.md manually (paste the content above)
# ... then continue:

# 7. Commit the output files and README
git add output/books.json output/errors.json output/run-report.json README.md
git commit -m "Add output evidence and complete README"

# 8. Push to GitHub
git push

```

