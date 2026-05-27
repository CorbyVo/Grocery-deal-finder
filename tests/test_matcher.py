from src.matcher import ProductMatcher
import pandas as pd

def test_exact_match_returns_same_product():
    matcher = ProductMatcher()
    match, score = matcher.match_product("milk", threshold=0.5)
    assert match == "milk"
    assert score is not None
    assert score >= 0.50

def test_semantic_match_spaghetti_maps_to_pasta():
    matcher = ProductMatcher()
    match, score = matcher.match_product("spaghetti", threshold=0.5)
    assert match == "pasta"
    assert score is not None
    assert score >= 0.50


