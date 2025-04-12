"""
main.py

Entry point for the Python Web Scraping Midterm Project.
Coordinates data collection, parsing, storage, and analysis.
"""
import os
import sys
import asyncio
import logging

from scraper.collector import Collector
from scraper.async_collector import AsyncCollector
from scraper.parser import Parser
from models.data_models import Book
from utils.file_handler import save_books_to_json, save_books_to_csv, load_books_from_json
from utils.analyzer import count_books_per_category, average_price_per_category, get_unavailable_books
from urllib.parse import urljoin, urlparse  # Added import for urljoin and urlparse
import os
import os


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", mode='w'),
        logging.StreamHandler() # Log to console as well
    ]
)

logger = logging.getLogger(__name__)


async def async_scrape():
    base_url = "http://books.toscrape.com/"
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    books = []
    async with AsyncCollector(base_url) as ac:
        allowed = await ac.check_robots_txt()
        if not allowed:
            print("Scraping disallowed by robots.txt. Exiting.")
            return
        paths = [""]  # Extend as needed
        responses = await ac.fetch_multi(paths)

        # Gather all book listing info
        raw_book_entries = []
        for path, html in responses.items():
            if not isinstance(html, str):
                print(f"Failed to fetch {path}: {html}")
                continue
            try:
                parser = Parser(html)
                titles = parser.get_all_titles()
                prices = parser.get_all_prices()
                urls = parser.get_product_links()
                availability_list = parser.get_availability_list()

                for title, price, url, availability in zip(titles, prices, urls, availability_list):
                    detail_url = urljoin(base_url, url)
                    parsed_detail_url = urlparse(detail_url).path.lstrip('/')
                    raw_book_entries.append({
                        "title": title,
                        "price": price,
                        "url": detail_url,
                        "availability": availability,
                        "fetch_path": parsed_detail_url,
                    })
            except Exception as err:
                print(f"Error processing path {path}: {err}")

        # Batch fetch all detail pages concurrently
        detail_fetch_tasks = [
            ac.fetch(entry["fetch_path"]) for entry in raw_book_entries
        ]
        detail_html_results = await asyncio.gather(*detail_fetch_tasks, return_exceptions=True)

        for entry, detail_result in zip(raw_book_entries, detail_html_results):
            if isinstance(detail_result, Exception):
                print(f"[DEBUG] Failed to fetch detail page for {entry['title']} at {entry['url']}: {detail_result}")
                category = "Unknown"
            else:
                try:
                    detail_parser = Parser(detail_result)
                    category = detail_parser.get_category_name() or "Unknown"
                    print(f"[DEBUG] Category for {entry['title']}: {category}")
                except Exception as exc:
                    print(f"[DEBUG] Error parsing category for {entry['title']} at {entry['url']}: {exc}")
                    category = "Unknown"
            book = Book(
                title=entry["title"],
                price=entry["price"],
                url=entry["url"],
                availability=entry["availability"],
                category=category
            )
            books.append(book)
        save_books_to_json(books, os.path.join(output_dir, "books.json"))
        save_books_to_csv(books, os.path.join(output_dir, "books.csv"))

    # No changes needed here, but ensure full content for completeness
    loaded_books = load_books_from_json(os.path.join(output_dir, "books.json"))
    print("\nBooks per category:")
    print(count_books_per_category(loaded_books))

    print("\nAverage price per category:")
    print(average_price_per_category(loaded_books))

    print("\nUnavailable books:")
    for book in get_unavailable_books(loaded_books):
        print(f"- {book.title}")


def sync_scrape():
    base_url = "http://books.toscrape.com/"
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    collector = Collector(base_url)
    if not collector.check_robots_txt():
        print("Scraping is disallowed by robots.txt. Exiting.")
        return

    html = collector.fetch()

    parser = Parser(html)
    titles = parser.get_all_titles()
    prices = parser.get_all_prices()
    urls = parser.get_product_links()
    availability_list = parser.get_availability_list()
    category_name = parser.get_category_name() or "Unknown"

    books = []
    from urllib.parse import urljoin, urlparse

    for title, price, url, availability in zip(titles, prices, urls, availability_list):
        # Ensure correct resolution of relative links (may have '../')
        # urljoin will handle '../', but path for fetch must not start with '/'
        detail_url = urljoin(base_url, url)
        parsed = urlparse(detail_url)
        fetch_path = parsed.path.lstrip('/')  # collector.fetch expects no leading slash

        print(f"[DEBUG] Book: {title} | href: {url} | detail_url: {detail_url} | fetch_path: {fetch_path}")

        try:
            detail_html = collector.fetch(fetch_path)
        except Exception as e:
            print(f"Failed to fetch detail page for {title} at {detail_url}: {e}")
            category = "Unknown"
        else:
            detail_parser = Parser(detail_html)
            category = detail_parser.get_category_name() or "Unknown"
            print(f"[DEBUG] Category for {title}: {category}")
        book = Book(
            title=title,
            price=price,
            url=detail_url,
            availability=availability,
            category=category
        )
        books.append(book)

    save_books_to_json(books, os.path.join(output_dir, "books.json"))
    save_books_to_csv(books, os.path.join(output_dir, "books.csv"))

    loaded_books = load_books_from_json(os.path.join(output_dir, "books.json"))
    print("\nBooks per category:")
    print(count_books_per_category(loaded_books))

    print("\nAverage price per category:")
    print(average_price_per_category(loaded_books))

    print("\nUnavailable books:")
    for book in get_unavailable_books(loaded_books):
        print(f"- {book.title}")


if __name__ == "__main__":
    if '--async' in sys.argv:
        print("Running in ASYNC scraping mode")
        asyncio.run(async_scrape())
    else:
        print("Running in SYNC scraping mode")
        sync_scrape()
