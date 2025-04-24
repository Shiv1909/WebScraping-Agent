 # tests/test_end_to_end.py

import pytest
from agent.search_tool import GoogleCSESearchTool
from agent.scraper_tool import WebScraperTool
from agent.content_analyzer import ContentAnalyzer
from agent.synthesizer import Synthesizer

@pytest.fixture
def mock_pipeline(monkeypatch):
    monkeypatch.setattr("google.generativeai.configure", lambda **kwargs: None)

    class MockSearch(GoogleCSESearchTool):
        def search(self, query, num_results=3):
            return [{"title": "Test", "link": "http://example.com", "snippet": "Snippet"}]

    class MockScraper(WebScraperTool):
        def scrape(self, url):
            return {"url": url, "content": "This is article content"}

    class MockAnalyzer(ContentAnalyzer):
        def analyze(self, content, url):
            return {"url": url, "summary": "Summarized content"}

    class MockSynthesizer(Synthesizer):
        def synthesize(self, articles, query):
            return "# Final Report\nSummary: Everything looks good."

    return MockSearch(), MockScraper(), MockAnalyzer(), MockSynthesizer()

def test_full_pipeline(mock_pipeline):
    search_tool, scraper, analyzer, synthesizer = mock_pipeline
    results = search_tool.search("Trade")
    articles = [analyzer.analyze(scraper.scrape(r["link"])["content"], r["link"]) for r in results]
    report = synthesizer.synthesize(articles, "Trade deal progress")
    assert "Final Report" in report
