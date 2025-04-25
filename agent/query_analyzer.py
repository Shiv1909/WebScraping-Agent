# agent/query_analyzer.py

from typing import Dict, List, Union
import google.generativeai as genai
from .config import GEMINI_API_KEY
import logging
import time
import ast

# ─── Logging Config ─────────────────────────────────────────────
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class QueryAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    def analyze_query(self, query: str) -> Dict[str, Union[str, List[List[str]]]]:
        """
        Uses Gemini to extract structured web search intent and keyword clusters.

        Returns:
            Dict with Intent, Info Types, Time Range, KeywordChunks
        """
        prompt = f"""
        You are a web research planning assistant. Break down the user query into:

        1. Intent: Describe what the user is trying to learn
        2. Info Types: Type of data/sources needed
        3. Time Range: Temporal scope (e.g., recent, past year)
        4. KeywordChunks: Group 2–5 related search phrases into Python-style list of lists

        User Query:
        \"\"\"{query}\"\"\"

        Format:
        Intent: ...
        Info Types: ...
        Time Range: ...
        KeywordChunks:
        [["term1", "term2"], ["group2a", "group2b"]]
        """

        try:
            response = self.model.generate_content(prompt)
            logger.info("Gemini query analysis succeeded")
            time.sleep(5)
            return self._parse_response(response.text.strip(), query)

        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            return {
                "Intent": "unknown",
                "Info Types": "general",
                "Time Range": "none",
                "KeywordChunks": [[query]]
            }

    def _parse_response(self, response_text: str, fallback_query: str) -> Dict[str, Union[str, List[List[str]]]]:
        result = {
            "Intent": "unknown",
            "Info Types": "general",
            "Time Range": "none",
            "KeywordChunks": [[fallback_query]]
        }

        lines = response_text.splitlines()
        chunk_lines = []
        inside_chunk = False

        for line in lines:
            if "KeywordChunks:" in line:
                inside_chunk = True
                continue
            if inside_chunk:
                chunk_lines.append(line)
            elif ':' in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()

        if chunk_lines:
            try:
                chunk_text = "\n".join(chunk_lines).strip()
                result["KeywordChunks"] = ast.literal_eval(chunk_text)
            except Exception as e:
                logger.warning(f"Failed to parse keyword chunks: {e}")
                result["KeywordChunks"] = [[fallback_query]]

        return result
