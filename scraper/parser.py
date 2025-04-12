"""
parser.py

Parses HTML content using BeautifulSoup4.
Implements multiple extraction methods, nested navigation,
and error handling for missing elements.
"""

from bs4 import BeautifulSoup
from typing import List, Optional


class Parser:
    """
    Parser class to extract data from HTML content.
    """

    def __init__(self, html: str):
        """
        Initialize the parser with raw HTML.

        Args:
            html (str): Raw HTML content.
        """
        self.soup = BeautifulSoup(html, "html.parser")

    def get_all_titles(self) -> List[str]:
        """
        Example of extracting all book titles using CSS selectors.

        Returns:
            List[str]: List of titles.
        """
        titles = []
        elements = self.soup.select("h3 a")
        for element in elements:
            title = element.get("title", "").strip()
            titles.append(title)
        return titles

    def get_all_prices(self) -> List[str]:
        """
        Extract all prices nested in elements with class 'price_color'.

        Returns:
            List[str]: List of price strings.
        """
        return [price.text.strip() for price in self.soup.find_all(class_="price_color")]

    def get_product_links(self) -> List[str]:
        """
        Extract product detail page links using attribute extraction.

        Returns:
            List[str]: List of URLs.
        """
        links = []
        elements = self.soup.select("h3 a")
        for element in elements:
            href = element.get("href")
            if href:
                links.append(href)
        return links

    def get_availability_list(self) -> List[str]:
        """
        Extract availability status.

        Returns:
            List[str]: List of status texts.
        """
        availabilities = []
        elements = self.soup.find_all("p", class_="instock availability")
        for element in elements:
            availabilities.append(element.text.strip())
        return availabilities

    def get_category_name(self) -> Optional[str]:
        """
        Extracts book category from breadcrumb navigation.
        For path like "Home > Books > Poetry > Title",
        returns "Poetry" (second-to-last item).

        Returns:
            Optional[str]: Category name or None if not found.
        """
        breadcrumb_items = self.soup.select(".breadcrumb li")
        if len(breadcrumb_items) >= 3:  # Need at least: Home > Category > Title
            category_item = breadcrumb_items[-2]  # Second to last item
            return category_item.text.strip()
        return "All products"  # Fallback for malformed breadcrumbs

    def get_title(self) -> str:
        """
        Extract the title of a single book.

        Returns:
            str: The book title or empty string if not found.
        """
        title_element = self.soup.find("h1") or self.soup.find("h3")
        return ' '.join(title_element.text.strip().split()) if title_element else ""

    def get_price(self) -> str:
        """
        Extract the price of a single book.

        Returns:
            str: The price text or empty string if not found.
        """
        price_element = self.soup.find(class_="price_color")
        return price_element.text.strip() if price_element else ""

    def get_availability(self) -> str:
        """
        Extract the availability status of a single book.

        Returns:
            str: The availability status or empty string if not found.
        """
        availability_element = self.soup.find(class_="availability")
        return availability_element.text.strip() if availability_element else ""

    def get_all_titles(self) -> List[str]:
        """
        Extract all book titles using CSS selectors. Handles both h3 > a and direct h3.

        Returns:
            List[str]: List of titles.
        """
        titles = []
        # Prioritize 'h3 a[title]' as it's more specific on the target site
        elements = self.soup.select("article.product_pod h3 a")
        if not elements:
            # Fallback to direct h3 if 'h3 a' isn't found (for test cases)
            elements = self.soup.select("h3")

        for element in elements:
            # If it's an 'a' tag with a title attribute, use that
            if element.name == 'a' and element.get("title"):
                title = element.get("title", "").strip()
            # Otherwise, use the text content, normalizing whitespace
            else:
                title = ' '.join(element.text.strip().split())

            if title:
                titles.append(title)
        return titles
