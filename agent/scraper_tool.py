# agent/scraper_tool.py

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

# ─── Logging Config ─────────────────────────────────────────────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WebScraperTool:
    def __init__(self, user_agent: str = "Mozilla/5.0"):
        self.headers = {"User-Agent": user_agent}

    def scrape(self, url: str) -> Dict[str, str]:
        """
        Scrapes clean text content (from <p> tags) from a webpage.

        Args:
            url (str): URL of the page to scrape

        Returns:
            Dict[str, str]: Dictionary with 'url' and clipped 'content'
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            if not paragraphs:
                logger.warning(f"No <p> tags found at: {url}")

            clean_text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text())

            return {
                "url": url,
                "content": clean_text[:5000]  # Limit content to avoid LLM overflow
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {"url": url, "content": ""}

        except Exception as e:
            logger.exception(f"Unexpected error scraping {url}")
            return {"url": url, "content": ""}
