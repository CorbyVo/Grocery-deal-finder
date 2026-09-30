import csv
from pathlib import Path

from src.meal_assistant.recipe_loader import load_recipes
from src.meal_assistant.recipe_retriever import RecipeRetriever


EVAL_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "recipe_retrieval_eval.csv"
)


def evaluate_retrieval():
    retriever = RecipeRetriever(load_recipes())
    correct = 0
    total = 0

    with EVAL_PATH.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            results = retriever.retrieve(row["query"], top_k=1)
            predicted_id = results[0]["recipe"]["id"]
            expected_id = row["expected_recipe_id"]

            is_correct = predicted_id == expected_id
            correct += int(is_correct)
            total += 1

            print(
                f"{row['query']}\n"
                f"Expected: {expected_id} | Predicted: {predicted_id}\n"
            )

    accuracy = correct / total if total else 0.0
    print(f"Top-1 accuracy: {correct}/{total} ({accuracy:.1%})")
    return accuracy


if __name__ == "__main__":
    evaluate_retrieval()