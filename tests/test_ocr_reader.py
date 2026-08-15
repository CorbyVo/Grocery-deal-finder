from src.ocr_reader import parse_shopping_items


def test_parse_shopping_items_removes_numbers_and_bullets():
    raw_text = """
    1. eggs
    2) milk
    - pasta
    * tomatoes
    """

    result = parse_shopping_items(raw_text)

    assert result == ["eggs", "milk", "pasta", "tomatoes"]


def test_parse_shopping_items_ignores_empty_lines():
    raw_text = """

    eggs

    milk

    """

    result = parse_shopping_items(raw_text)

    assert result == ["eggs", "milk"]