from src.meal_assistant.recipe_text import recipe_to_text


def test_recipe_to_text():
    recipe = {
        "title": "Tomato Pasta",
        "ingredients": [
            {"name": "pasta"},
            {"name": "pasta sauce"},
            {"name": "cheese"},
        ],
        "tags": ["vegetarian", "quick"],
        "preparation_minutes": 5,
        "cooking_minutes": 15,
    }

    expected = (
        "Tomato Pasta. Ingredients: pasta, pasta sauce, cheese. "
        "Tags: vegetarian, quick. "
        "Preparation: 5 minutes. Cooking: 15 minutes."
    )

    assert recipe_to_text(recipe) == expected