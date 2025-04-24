# Info merging + contradiction resolution # agent/synthesizer.py

from typing import List, Dict
import google.generativeai as genai
from .config import GEMINI_API_KEY
import logging
import time
logger = logging.getLogger(__name__)

class Synthesizer:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    def synthesize(self, articles: List[Dict[str, str]], query: str) -> str:
        try:
            combined = ""
            for i, article in enumerate(articles):
                combined += f"[Source {i+1}] {article['url']}\nSummary:\n{article['summary']}\n\n"

            prompt = f"""
            You are a senior research assistant. Your job is to synthesize findings from multiple article summaries related to the topic: "{query}".

            Steps:
            - Group common insights.
            - Highlight contradictions.
            - End with a single paragraph "Final Takeaway".

            Here are the article summaries:
            {combined}

            Provide a response in Markdown format.
            """

            response = self.model.generate_content(prompt)
            time.sleep(10)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            return "Synthesis failed."
