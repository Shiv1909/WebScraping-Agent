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

    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform a web search using Google CSE."""
        params = {
            "q": query,
            "cx": self.cse_id,
            "key": self.api_key,
            "num": num_results,
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = []

            for item in data.get("items", []):
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet", "")
                })

            return results

        except requests.exceptions.RequestException as e:
            logger.error(f"Search failed: {e}")
            return []

        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []
