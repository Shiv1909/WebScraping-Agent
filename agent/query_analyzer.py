from typing import Dict, List, Union
import google.generativeai as genai
from .config import GEMINI_API_KEY
import logging
import time
import ast  # ✅ safer than eval
logger = logging.getLogger(__name__)

class QueryAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    def analyze_query(self, query: str) -> Dict[str, Union[str, List[List[str]]]]:
        """Uses Gemini to extract structured search intent + grouped keyword chunks."""
        prompt = f"""
            You are a web research planning assistant. Break down the user query into:

            1. Intent: Describe what the user is trying to learn (e.g., 'news', 'comparison', 'status update')
            2. Info Types: Describe what type of sources/data should be retrieved
            3. Time Range: What time filters should apply (e.g., recent, past year)
            4. KeywordChunks: Group 2–5 related keyword phrases per cluster that can be used for targeted web search queries.

            The keyword groups should be returned as a valid Python list of lists, with no markdown formatting.

            User Query:
            \"\"\"
            {query}
            \"\"\"

            Expected format:
            Intent: ...
            Info Types: ...
            Time Range: ...
            KeywordChunks:
            [
            ["India US trade deal", "India US trade agreement"],
            ["India exports to US", "US imports from India"],
            ["USTR India", "Ministry of Commerce India"]
            ]
            """

        try:
            response = self.model.generate_content(prompt)
            print("🔍 Gemini response:\n", response.text.strip())
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

        # Parse the keyword chunks
        if chunk_lines:
            try:
                chunk_text = "\n".join(chunk_lines).strip()
                result["KeywordChunks"] = ast.literal_eval(chunk_text)
            except Exception as e:
                logger.warning(f"Failed to parse keyword chunks: {e}")
                result["KeywordChunks"] = [[fallback_query]]

        return result
