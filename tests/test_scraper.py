import unittest
import time  # Keep time import if needed by any retained async tests (though likely removed)
from scraper.parser import Parser
from scraper.async_collector import AsyncCollector  # Keep for potential future tests
import asyncio
from unittest.mock import patch, MagicMock  # Keep for potential future tests

class TestParser(unittest.TestCase):
    """Focuses on testing the Parser class functionality."""

    def test_category_extraction_from_breadcrumbs(self):
        """Test category extraction from different breadcrumb scenarios"""
        # Test normal breadcrumb path
        html_normal = """
        <ul class="breadcrumb">
            <li><a href="/">Home</a></li>
            <li><a href="/books">Books</a></li>
            <li><a href="/books/poetry">Poetry</a></li>
            <li class="active">A Light in the Attic</li>
        </ul>
        """
        parser_normal = Parser(html_normal)
        self.assertEqual(parser_normal.get_category_name(), "Poetry")

        # Test short breadcrumb (no proper category)
        html_short = """
        <ul class="breadcrumb">
            <li><a href="/">Home</a></li>
            <li class="active">A Light in the Attic</li>
        </ul>
        """
        parser_short = Parser(html_short)
        self.assertEqual(parser_short.get_category_name(), "All products") # Default fallback

        # Test empty breadcrumb
        html_empty = "<ul class=\"breadcrumb\"></ul>"
        parser_empty = Parser(html_empty)
        self.assertEqual(parser_empty.get_category_name(), "All products") # Default fallback

    def test_category_extraction_failure(self):
        """Test category extraction with malformed HTML"""
        html = "<ul class=\"breadcrumb\"><li>Only one item</li></ul>" # Malformed
        parser = Parser(html)
        self.assertEqual(parser.get_category_name(), "All products")  # Expect fallback

    def test_parser_initialization(self):
        """Test Parser initialization with basic HTML"""
        parser = Parser("<html><head></head><body><p>Test</p></body></html>")
        self.assertIsInstance(parser, Parser)
        self.assertIsNotNone(parser.soup)

    def test_get_title(self):
        """Test title extraction (including whitespace normalization)"""
        html_simple = "<h1>Test Title</h1>"
        parser_simple = Parser(html_simple)
        self.assertEqual(parser_simple.get_title(), "Test Title")

        html_spaced = "<h1>\n   Spaced    Title   \n</h1>"
        parser_spaced = Parser(html_spaced)
        # Uses the corrected get_title which normalizes whitespace
        self.assertEqual(parser_spaced.get_title(), "Spaced Title")

        html_nested = "<h1><span>Nested</span> Title</h1>"
        parser_nested = Parser(html_nested)
        self.assertEqual(parser_nested.get_title(), "Nested Title")

    def test_get_price(self):
        """Test price extraction"""
        html = "<p class=\"price_color\">£10.00</p>"
        parser = Parser(html)
        self.assertEqual(parser.get_price(), "£10.00")

        html_varied = "<p class=\"price_color\">$20.50</p>"
        parser_varied = Parser(html_varied)
        self.assertEqual(parser_varied.get_price(), "$20.50")

    def test_get_availability(self):
        """Test availability extraction"""
        html_instock = "<p class=\"availability\">In stock</p>"
        parser_instock = Parser(html_instock)
        self.assertIn("In stock", parser_instock.get_availability())

        html_outofstock = "<p class=\"availability\">Out of stock</p>"
        parser_outofstock = Parser(html_outofstock)
        self.assertIn("Out of stock", parser_outofstock.get_availability())

    def test_multi_book_parsing_titles(self):
        """Test parsing multiple book titles from a page (using corrected get_all_titles)"""
        # Test case simulating the structure from the website
        html_site = """
        <ol class="row">
            <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
                <article class="product_pod">
                    <h3><a href="catalogue/book1_1/index.html" title="Book One Title">Book One Title</a></h3>
                </article>
            </li>
            <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
                <article class="product_pod">
                    <h3><a href="catalogue/book2_2/index.html" title="Book Two Title">Book Two Title</a></h3>
                </article>
            </li>
        </ol>
        """
        parser_site = Parser(html_site)
        titles_site = parser_site.get_all_titles()
        self.assertIn("Book One Title", titles_site)
        self.assertIn("Book Two Title", titles_site)
        self.assertEqual(len(titles_site), 2)

        # Test case simulating the previous failing test structure
        html_simple_h3 = """
        <h3>Book1</h3><p class=\"price_color\">£10.00</p><p class=\"availability\">In stock</p>
        <h3>Book2</h3><p class=\"price_color\">£15.00</p><p class=\"availability\">Out of stock</p>
        """
        parser_simple_h3 = Parser(html_simple_h3)
        titles_simple_h3 = parser_simple_h3.get_all_titles()
        self.assertIn("Book1", titles_simple_h3)
        self.assertIn("Book2", titles_simple_h3)
        self.assertEqual(len(titles_simple_h3), 2)


    def test_price_parsing_edge_cases(self):
        """Test price parsing with edge cases (zero, non-numeric)"""
        html_zero = "<p class=\"price_color\">£0.00</p>"
        parser_zero = Parser(html_zero)
        self.assertEqual(parser_zero.get_price(), "£0.00")

        html_free = "<p class=\"price_color\">Free!</p>"
        parser_free = Parser(html_free)
        self.assertEqual(parser_free.get_price(), "Free!")

    def test_availability_edge_cases(self):
        """Test availability with edge cases (different text formats)"""
        variations = [
            ("<p class=\"availability\">In stock (5 available)</p>", "In stock (5 available)"),
            ("<p class=\"availability\">Limited stock</p>", "Limited stock"),
            ("<p class=\"availability\">Last copy!</p>", "Last copy!"),
        ]
        for html, expected in variations:
            parser = Parser(html)
            self.assertIn(expected, parser.get_availability())

    def test_empty_html(self):
        """Test handling of empty HTML input"""
        parser = Parser("")
        self.assertEqual(parser.get_title(), "")
        self.assertEqual(parser.get_price(), "")
        self.assertEqual(parser.get_availability(), "")
        self.assertEqual(parser.get_category_name(), "All products") # Should fallback
        self.assertEqual(parser.get_all_titles(), [])

if __name__ == "__main__":
    unittest.main()
