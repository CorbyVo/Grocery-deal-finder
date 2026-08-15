from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_ocr_shopping_list_endpoint(monkeypatch):
    def fake_extract_text_from_image(image_bytes):
        return "egss\nspagheti\ntomatos"

    def fake_parse_shopping_items(raw_text):
        return ["egss", "spagheti", "tomatos"]

    def fake_clean_items_with_llm(raw_text, fallback_items):
        return ["eggs", "spaghetti", "tomatoes"]

    monkeypatch.setattr("api.main.extract_text_from_image", fake_extract_text_from_image)
    monkeypatch.setattr("api.main.parse_shopping_items", fake_parse_shopping_items)
    monkeypatch.setattr("api.main.clean_items_with_llm", fake_clean_items_with_llm)

    response = client.post(
        "/ocr/shopping-list",
        files={
            "file": (
                "shopping_list.png",
                b"fake image content",
                "image/png"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "shopping_list.png"
    assert data["raw_text"] == "egss\nspagheti\ntomatos"
    assert data["raw_items"] == ["egss", "spagheti", "tomatos"]
    assert data["cleaned_items"] == ["eggs", "spaghetti", "tomatoes"]


def test_ocr_rejects_non_image_file():
    response = client.post(
        "/ocr/shopping-list",
        files={
            "file": (
                "shopping_list.txt",
                b"eggs\nmilk\npasta",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload an image file."