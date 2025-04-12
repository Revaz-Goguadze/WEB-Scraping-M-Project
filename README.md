# Python Web Scraping Midterm Project

A modular scraping and data analysis toolkit featuring asynchronous collection, GUI visualization, and robust testing.

## Features

- Async and synchronous scraping options
- Robots.txt compliance and polite rate limiting
- BeautifulSoup4 parsing with multiple selectors
- Object-oriented data modeling
- Saves data to CSV & JSON
- Data analysis tools (counts, averages, availability)
- Tkinter GUI to browse data and charts
- Matplotlib data visualizations
- Unit tests for key modules

## Setup

```bash
pip install -r requirements.txt
```

## Usage

**Scrape synchronously:**

```bash
python main.py
```

**Scrape asynchronously (example):**

```bash
python main.py --async
```


**Run GUI viewer:**

```bash
python gui.py
```

**Run tests:**

```bash
pytest tests/
```

## Project Structure

```
main.py
gui.py
scraper/
  collector.py
  async_collector.py
  parser.py
models/
  data_models.py
utils/
  file_handler.py
  analyzer.py
tests/
  test_scraper.py
data/
  books.json, books.csv
requirements.txt
README.md
REPORT.md
CONTRIBUTIONS.md
```

## Dependencies

- requests
- beautifulsoup4
- aiohttp (async requests)
- matplotlib (plots)
- pytest (testing)
- tkinter (standard lib, GUI)

## Notes

- Practicing ethical scraping with respect for robots.txt and server limits.
## Documented Limitations

- Does not handle JavaScript-rendered pages (static HTML only).
- Robots.txt parsing is simplistic; does not consider user-agent specific rules or crawl-delay.
- Assumes book page structure is consistent and fixed.
- No retry logic on failed requests.
- Minimal error reporting in GUI.

## Potential Improvements

- Add automatic retries/backoff on network failures.
- Improve robots.txt parsing with `robotparser` or external libs.
- Support paginated listings to scrape all pages.
- Add proxy support for large scraping runs.
- Improve GUI: filtering, search, export.
- Enhance test coverage for edge cases.
- Deployment via Docker for easier setup.

