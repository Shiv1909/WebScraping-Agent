# agent/query_analyzer.py

from typing import Dict
import google.generativeai as genai
from .config import GEMINI_API_KEY
import logging
import time
logger = logging.getLogger(__name__)

class QueryAnalyzer:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    def analyze_query(self, query: str) -> Dict[str, str]:
        """Uses Gemini to extract intent and keywords from user query."""
        prompt = f"""
Analyze the following user query and return a structured plan for web research.

User Query:
\"\"\"
{query}
\"\"\"

Extract:
1. Query Intent (e.g., 'news', 'facts', 'comparison', 'timeline')
2. Suggested Search Keywords
3. Required Information Types (e.g., statistics, recent news, official sources)
4. Any Time Constraints (e.g., past week, this year)

Format your output like this:
Intent: ...
Keywords: ...
Info Types: ...
Time Range: ...
"""

        try:
            response = self.model.generate_content(prompt)
            time.sleep(10)
            return self._parse_response(response.text.strip())
        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            return {
                "Intent": "unknown",
                "Keywords": query,
                "Info Types": "general",
                "Time Range": "none"
            }

    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Parse the Gemini output into structured dict."""
        lines = response_text.splitlines()
        result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
        return result
