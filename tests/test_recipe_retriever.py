from src.meal_assistant.recipe_loader import load_recipes
from src.meal_assistant.recipe_retriever import RecipeRetriever


def test_retrieve_returns_top_k_in_descending_order():
    recipes = load_recipes()
    retriever = RecipeRetriever(recipes)

    results = retriever.retrieve( "I want a breakfast with yogurt and fruit", top_k=2,)

    assert len(results) == 2
    assert results[0]["score"] >= results[1]["score"]
    assert results[0]["recipe"]["id"] != results[1]["recipe"]["id"]