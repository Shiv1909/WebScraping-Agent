# agent/search_tool.py

import requests
from typing import List, Dict, Optional
from urllib.parse import urlencode
import logging
from .config import GOOGLE_CSE_API_KEY, GOOGLE_CSE_CX

logger = logging.getLogger(__name__)

class GoogleCSESearchTool:
    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query: str, num_results: int = 10, max_pages: int = 2) -> List[Dict[str, str]]:
        """
        Perform a web search using Google CSE and fetch results across multiple pages.

        Args:
            query (str): Search query.
            num_results (int): Results per page (Google limits this to max 10).
            max_pages (int): How many pages to attempt (each page has up to 10 results).

        Returns:
            List of dicts: Each dict contains 'title', 'link', 'snippet', and 'page'.
        """
        results = []

        for page_num in range(max_pages):
            start = page_num * num_results + 1
            params = {
                "q": query,
                "cx": self.cse_id,
                "key": self.api_key,
                "num": num_results,
                "start": start
            }

            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                for item in data.get("items", []):
                    results.append({
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "snippet": item.get("snippet", ""),
                        "page": page_num + 1
                    })

            except requests.exceptions.RequestException as e:
                logger.error(f"Search failed on page {page_num + 1}: {e}")
                break

            except Exception as e:
                logger.error(f"Unexpected error during search on page {page_num + 1}: {e}")
                break

        return results
