def recipe_to_text(recipe):
    ingredient_names = [
        ingredient["name"]
        for ingredient in recipe["ingredients"]
    ]
    ingredients_text = ", ".join(ingredient_names)
    tags_text = ", ".join(recipe.get("tags", []))

    return (
        f"{recipe['title']}. "
        f"Ingredients: {ingredients_text}. "
        f"Tags: {tags_text}. "
        f"Preparation: {recipe['preparation_minutes']} minutes. "
        f"Cooking: {recipe['cooking_minutes']} minutes."
    )