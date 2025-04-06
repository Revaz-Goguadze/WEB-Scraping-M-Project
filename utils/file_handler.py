"""
file_handler.py

Handles saving and loading scraped data files (CSV, JSON)
with error handling.
"""

import csv
import json
from typing import List
from models.data_models import Book


def save_books_to_json(books: List[Book], filename: str):
    """
    Save list of Book objects to a JSON file.

    Args:
        books (List[Book]): List of Book objects.
        filename (str): Output filename.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in books], f, ensure_ascii=False, indent=4)
        print(f"Saved {len(books)} books to {filename}")
    except (IOError, TypeError) as e:
        print(f"Error saving JSON: {e}")


def load_books_from_json(filename: str) -> List[Book]:
    """
    Load list of Book objects from a JSON file.

    Args:
        filename (str): Input filename.

    Returns:
        List[Book]: List of Book objects.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Book(**item) for item in data]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return []


def save_books_to_csv(books: List[Book], filename: str):
    """
    Save list of Book objects to a CSV file.

    Args:
        books (List[Book]): List of Book objects.
        filename (str): Output filename.
    """
    try:
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "price", "url", "availability", "category"])
            writer.writeheader()
            for book in books:
                writer.writerow(book.to_dict())
        print(f"Saved {len(books)} books to {filename}")
    except IOError as e:
        print(f"Error saving CSV: {e}")


def load_books_from_csv(filename: str) -> List[Book]:
    """
    Load list of Book objects from a CSV file.

    Args:
        filename (str): Input filename.

    Returns:
        List[Book]: List of Book objects.
    """
    books = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(Book(**row))
    except IOError as e:
        print(f"Error loading CSV: {e}")
    return books