from io import BytesIO
import re
from PIL import Image, ImageOps
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes))

    # Simple preprocessing
    image = ImageOps.grayscale(image)

    text = pytesseract.image_to_string(image)

    return text


def parse_shopping_items(raw_text: str) -> list[str]:
    lines = raw_text.splitlines()

    items = []

    for line in lines:
        line = line.strip().lower()

        # remove bullets / numbers
        line = re.sub(r"^[\-\*\d\.\)\s]+", "", line)

        # remove empty lines
        if not line:
            continue

        items.append(line)

    return items