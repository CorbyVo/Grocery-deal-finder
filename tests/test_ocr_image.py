from io import BytesIO

import pytest
import pytesseract
from PIL import Image, ImageDraw, ImageFont

from src.ocr_reader import extract_text_from_image, parse_shopping_items


def create_test_image(text: str) -> bytes:
    image = Image.new("RGB", (600, 300), color="white")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except OSError:
        font = ImageFont.load_default()

    draw.text((40, 40), text, fill="black", font=font)

    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")

    return image_bytes.getvalue()


def test_extract_text_from_simple_printed_image():
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        pytest.skip("Tesseract OCR is not installed or not configured.")

    image_bytes = create_test_image("eggs\nmilk\npasta")

    raw_text = extract_text_from_image(image_bytes)
    items = parse_shopping_items(raw_text)

    assert "eggs" in items
    assert "milk" in items
    assert "pasta" in items