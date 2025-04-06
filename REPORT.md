# Python Web Scraping Midterm Project Report

## Website Chosen

Our team selected **http://books.toscrape.com/**, an open sandbox site designed for web scraping practice. This site offers predictable structure for books, multiple categories, and pagination, which facilitates the demonstration of scraping techniques without violating any terms or robots.txt.

## Implementation Highlights

We designed a modular scraping toolkit comprising:
- **Async HTTP collector** with error handling, headers, robots.txt compliance, and rate limiting.
- **BeautifulSoup4 parser** employing multiple selection techniques and nested DOM traversal.
- **Object-oriented models** (`Book`, `Category`) for data structure encapsulation.
- **File handlers** saving & loading JSON, CSV, with error management.
- **Analysis tools** providing per-category book counts, average pricing, and availability insights.
- **Tkinter GUI** to visualize scraped books.
- **Matplotlib plots** for category counts and price distributions.
- **Unit tests** ensuring reliability of scraping, parsing, file I/O, and analysis functions.

## Challenges Faced

- **Encoding issues** with currency symbols introduced errors when converting price strings; we fixed this by cleaning malformed bytes before parsing numeric values.
- **Robust parsing:** Handling missing elements gracefully was critical to avoid crashes; try/except blocks in parsing methods helped.
- **Concurrency:** Incorporating asynchronous HTTP requests required careful coordination of session management and respecting rate limits.
- **Visualization:** Selecting appropriate graph types for the scraped dataset, and ensuring compatibility with the Tkinter GUI loop.

## Analysis Performed

- Distribution of book counts across categories.
- Average book prices per category.
- Listing unavailable/out-of-stock books for potential consumer insights.

## Potential Improvements and Extensions

- Add pagination scraping to collect full datasets beyond the front page.
- Design machine learning modules to classify or cluster products.
- Expand to scrape multiple sites and unify data schemas.
- Deploy as a web service with user-initiated scraping jobs.
- Schedule automated updates using Cron or Celery workers.
- Package as a Python module or CLI tool.

## Conclusion

The project successfully demonstrates comprehensive scraping, structured data extraction, storage, analysis, and visualization, following good coding practices and teamwork. It lays a solid foundation for extension in the final project and beyond.