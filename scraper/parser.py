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
        Extracts category name by navigating breadcrumbs navigation.

        Returns:
            Optional[str]: Category name or None.
        """
        breadcrumb = self.soup.select_one(".breadcrumb li.active")
        if breadcrumb:
            return breadcrumb.text.strip()
        return None