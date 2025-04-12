"""
main.py

Entry point for the Python Web Scraping Midterm Project.
Coordinates data collection, parsing, storage, and analysis.
"""
import os
import sys
import asyncio
from scraper.collector import Collector
from scraper.async_collector import AsyncCollector
from scraper.parser import Parser
from models.data_models import Book
from utils.file_handler import save_books_to_json, save_books_to_csv, load_books_from_json
from utils.analyzer import count_books_per_category, average_price_per_category, get_unavailable_books
import os


async def async_scrape():
    base_url = "http://books.toscrape.com/"
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    async with AsyncCollector(base_url) as ac:
        allowed = await ac.check_robots_txt()
        if not allowed:
            print("Scraping disallowed by robots.txt. Exiting.")
            return
        # For demonstration only scrape first page
        paths = [""]  # can extend to /catalogue/page-1.html, page-2.html, etc
        responses = await ac.fetch_multi(paths)

    books = []
    for path, html in responses.items():
        if not isinstance(html, str):
            print(f"Failed to fetch {path}: {html}")
            continue
        parser = Parser(html)
        titles = parser.get_all_titles()
        prices = parser.get_all_prices()
        urls = parser.get_product_links()
        availability_list = parser.get_availability_list()
        category_name = parser.get_category_name() or "Unknown"

        for title, price, url, availability in zip(titles, prices, urls, availability_list):
            book = Book(
                title=title,
                price=price,
                url=url,
                availability=availability,
                category=category_name
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