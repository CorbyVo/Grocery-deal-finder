from unittest.mock import Mock
import requests
from src.llm_cleaner import clean_items_with_llm


def test_clean_items_with_llm_returns_cleaned_items(monkeypatch):
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "response": '{"items": ["eggs", "spaghetti", "tomatoes"]}'
    }

    def fake_post(*args, **kwargs):
        return fake_response

    monkeypatch.setattr(requests, "post", fake_post)

    raw_text = "egss\nspagheti\ntomatos"
    fallback_items = ["egss", "spagheti", "tomatos"]

    result = clean_items_with_llm(raw_text, fallback_items)

    assert result == ["eggs", "spaghetti", "tomatoes"]


def test_clean_items_with_llm_uses_fallback_when_ollama_fails(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Ollama is not running")

    monkeypatch.setattr(requests, "post", fake_post)

    raw_text = "eggs\nmilk"
    fallback_items = ["eggs", "milk"]

    result = clean_items_with_llm(raw_text, fallback_items)

    assert result == ["eggs", "milk"]