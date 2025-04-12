import unittest
from scraper.parser import Parser


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


if __name__ == "__main__":
    unittest.main()
