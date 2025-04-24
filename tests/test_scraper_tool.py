 # tests/test_scraper_tool.py

import pytest
from agent.scraper_tool import WebScraperTool

@pytest.fixture
def scraper():
    return WebScraperTool()

def test_scrape_html(monkeypatch, scraper):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            text = "<html><body><p>Test paragraph</p></body></html>"
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    result = scraper.scrape("https://ai.google.dev/gemini-api/docs/models")
    
    assert "Test paragraph" in result["content"]
