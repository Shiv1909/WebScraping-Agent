 # tests/test_content_analyzer.py

import pytest
from agent.content_analyzer import ContentAnalyzer

@pytest.fixture
def analyzer(monkeypatch):
    class MockModel:
        def generate_content(self, prompt): return type("Mock", (), {"text": "Mock summary"})()

    monkeypatch.setattr("google.generativeai.configure", lambda **kwargs: None)
    monkeypatch.setattr("google.generativeai.GenerativeModel", lambda model_name: MockModel())

    return ContentAnalyzer()

def test_analyze_returns_summary(analyzer):
    result = analyzer.analyze("Some article text", "http://example.com")
    assert "Mock summary" in result["summary"]
