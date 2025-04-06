"""
analyzer.py

Provides data analysis tools on scraped data.
"""

from typing import List, Dict
from models.data_models import Book


def count_books_per_category(books: List[Book]) -> Dict[str, int]:
    """
    Count books grouped by category.

    Args:
        books (List[Book]): List of Book objects.

    Returns:
        Dict[str, int]: Mapping of category to count.
    """
    counts = {}
    for book in books:
        cat = book.category
        counts[cat] = counts.get(cat, 0) + 1
    return counts


def average_price_per_category(books: List[Book]) -> Dict[str, float]:
    """
    Compute average price per category.

    Args:
        books (List[Book]): List of Book objects.

    Returns:
        Dict[str, float]: Category to average price mapping.
    """
    sums = {}
    counts = {}
    for book in books:
        cat = book.category
        price_str = book.price.strip().replace('Â', '').replace('£', '').replace('$', '')
        try:
            price_val = float(price_str)
        except ValueError:
            continue
        sums[cat] = sums.get(cat, 0.0) + price_val
        counts[cat] = counts.get(cat, 0) + 1
    averages = {}
    for cat in sums:
        averages[cat] = sums[cat] / counts[cat]
    return averages


def get_unavailable_books(books: List[Book]) -> List[Book]:
    """
    List books that are currently unavailable/out of stock.

    Args:
        books (List[Book]): List of Book objects.

    Returns:
        List[Book]: List of unavailable Book objects.
    """
    return [book for book in books if 'out of stock' in book.availability.lower()]