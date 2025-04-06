"""
data_models.py

Defines data structures for scraped information 
using object-oriented principles.
"""

from typing import List


class Book:
    """
    Class representing information about a book.
    """

    def __init__(self, title: str, price: str, url: str, availability: str, category: str):
        """
        Initialize a Book object.

        Args:
            title (str): Book title.
            price (str): Price string.
            url (str): URL to book detail page.
            availability (str): Availability status.
            category (str): Category of the book.
        """
        self.title = title
        self.price = price
        self.url = url
        self.availability = availability
        self.category = category

    def to_dict(self) -> dict:
        """
        Convert to dictionary format.

        Returns:
            dict: Data of the book.
        """
        return {
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "availability": self.availability,
            "category": self.category
        }


class Category:
    """
    Class representing a category of books.
    """

    def __init__(self, name: str):
        """
        Initialize a Category.

        Args:
            name (str): Name of the category.
        """
        self.name = name
        self.books: List[Book] = []

    def add_book(self, book: Book):
        """
        Add a book to the category.

        Args:
            book (Book): Book object to add.
        """
        self.books.append(book)

    def get_books(self) -> List[Book]:
        """
        Get books in this category.

        Returns:
            List[Book]: List of Book objects.
        """
        return self.books