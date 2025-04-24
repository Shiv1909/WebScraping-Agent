# Gemini summarizer + reliability check # agent/content_analyzer.py

from typing import Dict
import logging
import google.generativeai as genai
from .config import GEMINI_API_KEY
import time
logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

def analyze(self, content: str, url: str, original_query: str) -> Dict[str, str]:
    try:
        prompt = f"""
        You're an AI research assistant. Read the article below and do 3 things:

        1. Summarize it in 3-5 bullet points.
        2. Label the type of content (e.g., 'news report', 'opinion article', 'government page').
        3. Rate its relevance to the topic '{original_query}' (high/medium/low).

        Article Content:
        \"\"\"
        {content}
        \"\"\"
        """
        response = self.model.generate_content(prompt)
        return {
            "url": url,
            "summary": response.text.strip()
        }

    except Exception as e:
        logger.error(f"Gemini summarization failed for {url}: {e}")
        return {
            "url": url,
            "summary": "Summarization failed."
        }

