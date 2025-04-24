# BeautifulSoup / Selenium wrapper # agent/scraper_tool.py

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class WebScraperTool:
    def __init__(self, user_agent: str = "Mozilla/5.0"):
        self.headers = {"User-Agent": user_agent}

    def scrape(self, url: str) -> Dict[str, str]:
        """Scrapes the main content from a webpage."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Heuristic: extract visible <p> tags
            paragraphs = soup.find_all("p")
            clean_text = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text())

            return {
                "url": url,
                "content": clean_text[:5000]  # Clip to safe LLM context
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return {"url": url, "content": ""}

        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {"url": url, "content": ""}
