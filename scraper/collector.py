"""
collector.py

Handles HTTP requests with headers, respects robots.txt, 
and implements basic rate limiting and error handling.
"""

import requests
import time
from urllib.parse import urlparse


class Collector:
    """
    Collector class to fetch web pages with respect to request policies.
    """

    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Initialize a collector.

        Args:
            base_url (str): The base URL of the website.
            delay (float): Delay between requests in seconds.
        """
        self.base_url = base_url
        self.delay = delay
        self.last_request_time = None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MidtermScraperBot/1.0 (+https://example.com/bot)"
        })

    def respect_rate_limit(self):
        """
        Enforces delay between requests to avoid overwhelming the server.
        """
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

    def fetch(self, path: str = '') -> str:
        """
        Fetch a page from the website.

        Args:
            path (str): URL path to fetch (optional).

        Returns:
            str: The HTML content of the page.

        Raises:
            requests.RequestException: If a network error occurs.
        """
        self.respect_rate_limit()
        url = self.base_url + path
        try:
            response = self.session.get(url)
            response.raise_for_status()
            self.last_request_time = time.time()
            return response.text
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def check_robots_txt(self) -> bool:
        """
        Checks robots.txt for scraping permission.

        Returns:
            bool: True if scraping is allowed, False otherwise.
        """
        parsed = urlparse(self.base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            response = self.session.get(robots_url)
            if response.status_code != 200:
                # If no robots.txt, assume allowed
                return True
            content = response.text.lower()
            # Simplisitc check for Disallow
            if "disallow: /" in content:
                return False
            return True
        except requests.RequestException:
            # Assume allowed if can't fetch robots.txt
            return True