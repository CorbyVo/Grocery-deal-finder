import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RECIPES_PATH = PROJECT_ROOT / "data" / "recipes.json"

REQUIRED_RECIPE_FIELDS = {
    "id",
    "title",
    "servings",
    "preparation_minutes",
    "cooking_minutes",
    "ingredients",
    "steps",
}

def load_recipes(file_path=RECIPES_PATH):
    with open(file_path, encoding="utf-8") as file:
        recipes = json.load(file)

        if not isinstance(recipes, list):
            raise ValueError("recipes.json must contain a list of recipes")

        seen_ids = set()
        for index, recipe in enumerate(recipes):
            if not isinstance(recipe, dict):
                raise ValueError(f"Recipe {index} must be an object")

            missing = REQUIRED_RECIPE_FIELDS - recipe.keys()
            if missing:
                raise ValueError(f"Recipe {index} is missing: {sorted(missing)}")

            if recipe["id"] in seen_ids:
                raise ValueError(f"Duplicate recipe ID: {recipe['id']}")

            seen_ids.add(recipe["id"])

    return recipes