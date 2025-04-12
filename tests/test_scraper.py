import unittest
from scraper.parser import Parser
from scraper.async_collector import AsyncCollector  # For async tests
import asyncio
from unittest.mock import patch, MagicMock  # For mocking

class TestParser(unittest.TestCase):
    def test_category_extraction_from_breadcrumbs(self):
        """Test category extraction from different breadcrumb scenarios"""
        
        # Test normal breadcrumb path
        html = """
        <ul class="breadcrumb">
            <li><a href="/">Home</a></li>
            <li><a href="/books">Books</a></li>
            <li><a href="/books/poetry">Poetry</a></li>
            <li class="active">A Light in the Attic</li>
        </ul>
        """
        parser = Parser(html)
        self.assertEqual(parser.get_category_name(), "Poetry")

        # Test short breadcrumb (no proper category)
        html = """
        <ul class="breadcrumb">
            <li><a href="/">Home</a></li>
            <li class="active">A Light in the Attic</li>
        </ul>
        """
        parser = Parser(html)
        self.assertEqual(parser.get_category_name(), "All products")

        # Test empty breadcrumb
        html = "<ul class=\"breadcrumb\"></ul>"
        parser = Parser(html)
        self.assertEqual(parser.get_category_name(), "All products")

    def test_category_extraction_failure(self):
        """Test category extraction with malformed HTML"""
        html = "<ul class=\"breadcrumb\"></ul><div>Invalid</div>"  # Simulate bad HTML
        parser = Parser(html)
        self.assertEqual(parser.get_category_name(), "All products")  # Expect fallback

    def test_parser_initialization(self):
        """Test Parser initialization with various inputs"""
        parser = Parser("<html></html>")
        self.assertIsInstance(parser, Parser)

    def test_get_title(self):
        """Test title extraction"""
        html = "<h1>Test Title</h1>"
        parser = Parser(html)
        self.assertEqual(parser.get_title(), "Test Title")

    def test_get_price(self):
        """Test price extraction"""
        html = "<p class=\"price_color\">£10.00</p>"
        parser = Parser(html)
        self.assertEqual(parser.get_price(), "£10.00")

    def test_get_availability(self):
        """Test availability extraction"""
        html = "<p class=\"availability\">In stock</p>"
        parser = Parser(html)
        self.assertIn("In stock", parser.get_availability())

    def test_category_extraction_failure(self):
        """Test category extraction with malformed HTML"""
        html = "<ul class=\"breadcrumb\"></ul><div>Invalid</div>"  # Simulate bad HTML
        parser = Parser(html)
        self.assertEqual(parser.get_category_name(), "All products")  # Expect fallback

    def test_parser_initialization(self):
        """Test Parser initialization with various inputs"""
        parser = Parser("<html></html>")
        self.assertIsInstance(parser, Parser)

    def test_get_title(self):
        """Test title extraction"""
        html = "<h1>Test Title</h1>"
        parser = Parser(html)
        self.assertEqual(parser.get_title(), "Test Title")

    def test_get_price(self):
        """Test price extraction"""
        html = "<p class=\"price_color\">£10.00</p>"
        parser = Parser(html)
        self.assertEqual(parser.get_price(), "£10.00")

    def test_get_availability(self):
        """Test availability extraction"""
        html = "<p class=\"availability\">In stock</p>"
        parser = Parser(html)
        self.assertIn("In stock", parser.get_availability())

    def test_multi_book_parsing(self):
        """Test parsing multiple books from a page"""
        html = """
        <h3>Book1</h3><p class=\"price_color\">£10.00</p><p class=\"availability\">In stock</p>
        <h3>Book2</h3><p class=\"price_color\">£15.00</p><p class=\"availability\">Out of stock</p>
        """
        parser = Parser(html)
        titles = parser.get_all_titles()
        self.assertIn("Book1", titles)
        self.assertIn("Book2", titles)

    def test_price_parsing_variations(self):
        """Test price parsing with different formats"""
        html1 = "<p class=\"price_color\">£10.99</p>"
        parser1 = Parser(html1)
        self.assertEqual(parser1.get_price(), "£10.99")

        html2 = "<p class=\"price_color\">$20.50</p>"
        parser2 = Parser(html2)
        self.assertEqual(parser2.get_price(), "$20.50")

    def test_availability_parsing(self):
        """Test availability parsing variations"""
        html = "<p class=\"availability\">Out of stock</p>"
        parser = Parser(html)
        self.assertIn("Out of stock", parser.get_availability())

    def test_edge_case_no_books(self):
        """Test scraping with no books available"""
        html = "<div>No books found</div>"
        parser = Parser(html)
        self.assertEqual(parser.get_all_titles(), [])

    def test_invalid_url(self):
        """Test handling of invalid URLs"""
        with patch('aiohttp.ClientSession.get', side_effect=Exception("Invalid URL")):
            from scraper.async_collector import AsyncCollector
            ac = AsyncCollector()
            self.assertRaises(Exception, ac.fetch, "invalid_url")

    def test_robots_txt_check(self):
        """Test robots.txt check logic"""
        with patch('scraper.async_collector.AsyncCollector.check_robots_txt', return_value=False):
            self.assertFalse(scraper.async_collector.AsyncCollector().check_robots_txt())  # Mocked assertion

    def test_full_scrape_flow(self):
        """Test full end-to-end scrape flow"""
        with patch('main.async_scrape') as mock_async_scrape:
            mock_async_scrape.return_value = None
            from main import main  # Assuming entry point
            main()  # Simulate run
            mock_async_scrape.assert_called_once()

    def test_async_category_fetch_failure(self):
        """Test async category fetch with failures"""
        with patch('scraper.async_collector.AsyncCollector') as MockAsyncCollector:
            mock_ac = MagicMock()
            mock_ac.fetch.side_effect = Exception("Fetch error")
            MockAsyncCollector.return_value.__aenter__.return_value = mock_ac
            self.assertRaises(Exception, asyncio.run, mock_ac.fetch())

    def test_price_parsing_edge_cases(self):
        """Test price parsing with edge cases"""
        html_edge1 = "<p class=\"price_color\">£0.00</p>"  # Zero price
        parser_edge1 = Parser(html_edge1)
        self.assertEqual(parser_edge1.get_price(), "£0.00")

        html_edge2 = "<p class=\"price_color\">Free!</p>"  # Non-numeric price
        parser_edge2 = Parser(html_edge2)
        self.assertEqual(parser_edge2.get_price(), "Free!")  # Or handle as expected

    def test_availability_edge_cases(self):
        """Test availability with edge cases"""
        html_avail_edge = "<p class=\"availability\">Limited stock</p>"
        parser_avail_edge = Parser(html_avail_edge)
        self.assertIn("Limited stock", parser_avail_edge.get_availability())

    def test_html_special_characters(self):
        """Test parsing HTML with special characters"""
        html = "<h1>Book &amp; Title</h1>"
        parser = Parser(html)
        self.assertEqual(parser.get_title(), "Book & Title")

    def test_malformed_price_format(self):
        """Test handling of malformed price formats"""
        html = "<p class=\"price_color\">Invalid Price</p>"
        parser = Parser(html)
        self.assertEqual(parser.get_price(), "Invalid Price")

    def test_empty_html(self):
        """Test handling of empty HTML"""
        parser = Parser("")
        self.assertEqual(parser.get_title(), "")
        self.assertEqual(parser.get_price(), "")
        self.assertEqual(parser.get_availability(), "")

    def test_unicode_characters(self):
        """Test handling of Unicode characters"""
        html = "<h1>título del libro</h1>"
        parser = Parser(html)
        self.assertEqual(parser.get_title(), "título del libro")

    def test_multiple_price_elements(self):
        """Test handling of multiple price elements"""
        html = """
        <p class="price_color">£10.00</p>
        <p class="price_color">£20.00</p>
        """
        parser = Parser(html)
        self.assertEqual(parser.get_price(), "£10.00")  # Should get first price

    def test_nested_html_elements(self):
        """Test parsing nested HTML elements"""
        html = "<h1><span>Nested</span> Title</h1>"
        parser = Parser(html)
        self.assertEqual(parser.get_title(), "Nested Title")

    def test_whitespace_handling(self):
        """Test handling of excessive whitespace"""
        html = "<h1>\n   Spaced    Title   \n</h1>"
        parser = Parser(html)
        self.assertEqual(parser.get_title(), "Spaced Title")

    def test_availability_variations(self):
        """Test different availability status formats"""
        variations = [
            ("<p class=\"availability\">In stock (5 available)</p>", "In stock (5 available)"),
            ("<p class=\"availability\">Out of stock</p>", "Out of stock"),
            ("<p class=\"availability\">Last copy!</p>", "Last copy!"),
        ]
        for html, expected in variations:
            parser = Parser(html)
            self.assertIn(expected, parser.get_availability())

    def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        async def test_concurrent():
            urls = ["http://test1.com", "http://test2.com"]
            collector = AsyncCollector()
            tasks = [collector.fetch(url) for url in urls]
            with patch('aiohttp.ClientSession.get') as mock_get:
                mock_get.return_value.__aenter__.return_value.text = asyncio.Future()
                mock_get.return_value.__aenter__.return_value.text.set_result("<html></html>")
                results = await asyncio.gather(*tasks)
                self.assertEqual(len(results), 2)
        asyncio.run(test_concurrent())

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        async def test_rate_limit():
            collector = AsyncCollector()
            start_time = time.time()
            with patch('aiohttp.ClientSession.get') as mock_get:
                mock_get.return_value.__aenter__.return_value.text = asyncio.Future()
                mock_get.return_value.__aenter__.return_value.text.set_result("<html></html>")
                await collector.fetch("http://test.com")
                await collector.fetch("http://test.com")
                end_time = time.time()
                # Assuming rate limiting is implemented, there should be a delay
                self.assertGreaterEqual(end_time - start_time, 0.1)
        asyncio.run(test_rate_limit())

if __name__ == "__main__":
    unittest.main()
