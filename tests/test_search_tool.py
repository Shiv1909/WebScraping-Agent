 # tests/test_search_tool.py

import pytest
from agent.search_tool import GoogleCSESearchTool

@pytest.fixture
def search_tool():
    return GoogleCSESearchTool(api_key="test_api_key", cse_id="test_cse_id")

def test_search_returns_list(monkeypatch, search_tool):
    # Mocked search response
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self):
                return {
                    "items": [
                        {"title": "Test Title", "link": "http://example.com", "snippet": "Test snippet"}
                    ]
                }
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    results = search_tool.search("India US trade")
    
    assert isinstance(results, list)
    assert results[0]["title"] == "Test Title"
