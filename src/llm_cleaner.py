import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def clean_items_with_llm(raw_text: str, fallback_items: list[str]) -> list[str]:
    """
    Use a local LLM to clean OCR text into grocery items.
    If Ollama fails, return fallback_items.
    """

    prompt = f"""
You are cleaning an OCR result from a grocery shopping list.

Task:
- Extract only grocery product names.
- Fix obvious spelling mistakes.
- Remove quantities, prices, bullets, and noise.
- Return ONLY valid JSON.
- JSON format must be:
{{"items": ["item1", "item2"]}}

OCR text:
{raw_text}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        llm_response = data.get("response", "")

        parsed = json.loads(llm_response)
        items = parsed.get("items", [])

        if not isinstance(items, list):
            return fallback_items

        cleaned_items = [
            str(item).strip().lower()
            for item in items
            if str(item).strip()
        ]

        return cleaned_items if cleaned_items else fallback_items

    except Exception:
        return fallback_items