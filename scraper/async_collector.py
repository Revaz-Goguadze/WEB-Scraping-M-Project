"""
async_collector.py

Asynchronous web page fetcher using aiohttp.
"""

import aiohttp
import asyncio
from urllib.parse import urlparse


class AsyncCollector:
    """
    AsyncCollector is designed to fetch multiple pages concurrently with respect for robots.txt.
    """

    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Initialize AsyncCollector.

        Args:
            base_url (str): Base website URL.
            delay (float): Delay between requests (seconds).
        """
        self.base_url = base_url
        self.delay = delay
        self.session = None

    async def __aenter__(self):
        headers = {
            "User-Agent": "MidtermScraperBot/1.0 (+https://example.com/bot)"
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, url_suffix: str = "") -> str:
        """
        Fetch a single page asynchronously.

        Args:
            url_suffix (str): URL path or slug.

        Returns:
            str: HTML content.

        Raises:
            aiohttp.ClientError: If a network-related error occurs.
            asyncio.TimeoutError: If the request times out.
        """
        url = self.base_url + url_suffix
        try:
            async with self.session.get(url) as resp:
                resp.raise_for_status()
                await asyncio.sleep(self.delay)
                return await resp.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Request failed: {e}")
            raise

    async def fetch_multi(self, paths: list) -> dict:
        """
        Fetch multiple paths concurrently.

        Args:
            paths (list): URL suffixes.

        Returns:
            dict: Mapping path -> content (str).
        """
        tasks = [self.fetch(p) for p in paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {p: r for p, r in zip(paths, results)}

    async def check_robots_txt(self) -> bool:
        """
        Checks robots.txt compliance async.

        Returns:
            bool: Allowed or not.
        """
        parsed = urlparse(self.base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            async with self.session.get(robots_url) as resp:
                if resp.status != 200:
                    return True
                text = await resp.text()
                if "Disallow: /" in text:
                    return False
                return True
        except:
            return True