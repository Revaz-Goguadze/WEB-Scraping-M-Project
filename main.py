"""
main.py

Entry point for the Python Web Scraping Midterm Project.
Coordinates data collection, parsing, storage, and analysis.
"""

from scraper.collector import Collector
from scraper.parser import Parser
from models.data_models import Book
from utils.file_handler import save_books_to_json, save_books_to_csv, load_books_from_json
from utils.analyzer import count_books_per_category, average_price_per_category, get_unavailable_books
import os


def main():
    base_url = "http://books.toscrape.com/"
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    collector = Collector(base_url)
    if not collector.check_robots_txt():
        print("Scraping is disallowed by robots.txt. Exiting.")
        return

    # Fetch home page or category page (can expand for paging)
    html = collector.fetch()

    parser = Parser(html)
    titles = parser.get_all_titles()
    prices = parser.get_all_prices()
    urls = parser.get_product_links()
    availability_list = parser.get_availability_list()
    category_name = parser.get_category_name() or "Unknown"

    books = []
    for title, price, url, availability in zip(titles, prices, urls, availability_list):
        book = Book(
            title=title,
            price=price,
            url=url,
            availability=availability,
            category=category_name
        )
        books.append(book)

    # Save scraped data
    save_books_to_json(books, os.path.join(output_dir, "books.json"))
    save_books_to_csv(books, os.path.join(output_dir, "books.csv"))

    # Load from saved JSON and analyze
    loaded_books = load_books_from_json(os.path.join(output_dir, "books.json"))
    print("\nBooks per category:")
    print(count_books_per_category(loaded_books))

    print("\nAverage price per category:")
    print(average_price_per_category(loaded_books))

    print("\nUnavailable books:")
    for book in get_unavailable_books(loaded_books):
        print(f"- {book.title}")


if __name__ == "__main__":
    main()