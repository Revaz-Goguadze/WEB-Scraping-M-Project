"""
Basic unittest module for scraper project.
"""

import unittest
from scraper.parser import Parser
from utils.analyzer import count_books_per_category, average_price_per_category, get_unavailable_books
from models.data_models import Book


class TestParser(unittest.TestCase):
    def setUp(self):
        # example minimal HTML simulating BooksToScrape
        self.html = '''
        <html>
            <body>
                <h3><a title="Test Book" href="url">A title</a></h3>
                <p class="price_color">£10.00</p>
                <p class="instock availability">In stock</p>
                <ul class="breadcrumb"><li></li><li></li><li class="active">CategoryX</li></ul>
            </body>
        </html>
        '''
        self.parser = Parser(self.html)

    def test_titles(self):
        titles = self.parser.get_all_titles()
        self.assertIn('Test Book', titles)

    def test_prices(self):
        prices = self.parser.get_all_prices()
        self.assertIn('£10.00', prices)

    def test_links(self):
        links = self.parser.get_product_links()
        self.assertIn('url', links)

    def test_category(self):
        self.assertEqual(self.parser.get_category_name(), 'CategoryX')


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book("Book1", "£10.0", "url1", "In stock", "CategoryA"),
            Book("Book2", "£20.0", "url2", "out of stock", "CategoryA"),
            Book("Book3", "£15.0", "url3", "In stock", "CategoryB"),
        ]

    def test_counts(self):
        counts = count_books_per_category(self.books)
        self.assertEqual(counts["CategoryA"], 2)
        self.assertEqual(counts["CategoryB"], 1)

    def test_averages(self):
        avgs = average_price_per_category(self.books)
        self.assertAlmostEqual(avgs["CategoryA"], 15.0)
        self.assertAlmostEqual(avgs["CategoryB"], 15.0)

    def test_unavailable(self):
        unavail = get_unavailable_books(self.books)
        self.assertEqual(len(unavail), 1)
        self.assertEqual(unavail[0].title, "Book2")


if __name__ == '__main__':
    unittest.main()