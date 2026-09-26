from src.meal_assistant.recipe_loader import load_recipes
import pytest
import json
from pathlib import Path
import csv

def test_load_recipes_returns_tomato_pasta():
    recipes = load_recipes()

    assert isinstance(recipes, list)
    assert recipes[0]["id"] == "tomato-pasta"
    assert recipes[0]["title"] == "Tomato Pasta"
    assert len(recipes[0]["ingredients"]) == 3
    assert recipes[1]["id"] == "banana-yogurt-bowl"
    assert recipes[1]["ingredients"][1]["name"] == "bananas"
    assert len(recipes) == 3
    assert recipes[2]["id"] == "cheese-omelette"

def test_load_recipes_rejects_non_list(tmp_path):
    bad_file = tmp_path / "recipes.json"
    bad_file.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="must contain a list"):
        load_recipes(bad_file)

def test_load_recipes_rejects_missing_ingredients(tmp_path):
    bad_file = tmp_path / "recipes.json"
    bad_file.write_text('[{"id": "test-recipe"}]', encoding="utf-8")

    with pytest.raises(ValueError, match="missing"):
        load_recipes(bad_file)

def test_load_recipes_rejects_duplicate_ids(tmp_path):
    recipe = load_recipes()[0]
    bad_file = tmp_path / "recipes.json"
    bad_file.write_text(json.dumps([recipe, recipe]), encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate recipe ID"):
        load_recipes(bad_file)

def test_recipe_ingredients_exist_in_product_catalog():
    products_path = Path(__file__).resolve().parents[1] / "data" / "products.csv"

    with products_path.open(newline="", encoding="utf-8") as file:
        products = {
            int(row["product_id"]): row["normalized_name"]
            for row in csv.DictReader(file)
        }

    for recipe in load_recipes():
        for ingredient in recipe["ingredients"]:
            assert products[ingredient["product_id"]] == ingredient["name"]