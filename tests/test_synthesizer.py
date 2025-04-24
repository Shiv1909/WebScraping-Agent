 # tests/test_synthesizer.py

import pytest
from agent.synthesizer import Synthesizer

@pytest.fixture
def synthesizer(monkeypatch):
    class MockModel:
        def generate_content(self, prompt): return type("Mock", (), {"text": "# Summary\nMocked synthesis"})()

    monkeypatch.setattr("google.generativeai.configure", lambda **kwargs: None)
    monkeypatch.setattr("google.generativeai.GenerativeModel", lambda model_name: MockModel())

    return Synthesizer()

def test_synthesis_output(synthesizer):
    articles = [
        {"url": "http://1.com", "summary": "Summary 1"},
        {"url": "http://2.com", "summary": "Summary 2"},
    ]
    output = synthesizer.synthesize(articles, "India US trade deal")
    assert "Mocked synthesis" in output
