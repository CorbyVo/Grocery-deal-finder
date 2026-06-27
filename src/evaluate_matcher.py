from pathlib import Path
import pandas as pd
from src.matcher import ProductMatcher

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def normalize_expected(value):
    if pd.isna(value):
        return None

    value = str(value).strip()
    if value == "":
        return None

    return value


def evaluate_matcher(eval_path=None, threshold=0.50):
    if eval_path is None:
        eval_path = PROJECT_ROOT / "data" / "matcher_eval.csv"

    df = pd.read_csv(eval_path)
    matcher = ProductMatcher()

    results = []
    correct_count = 0

    for _, row in df.iterrows():
        user_input = row["user_input"]
        expected_match = normalize_expected(row["expected_match"])

        prediction = matcher.match_product_detailed(user_input, threshold=threshold)
        predicted_match = prediction["best_match"]

        is_correct = predicted_match == expected_match
        if is_correct:
            correct_count += 1

        results.append(
            {
                "user_input": user_input,
                "expected_match": expected_match,
                "predicted_match": predicted_match,
                "score": prediction["score"],
                "confidence": prediction["confidence"],
                "method": prediction["method"],
                "is_correct": is_correct,
            }
        )

    results_df = pd.DataFrame(results)
    accuracy = correct_count / len(results_df)

    print("Evaluation Results")
    print(results_df)
    print()
    print(f"Accuracy: {accuracy:.2%}")

    return results_df, accuracy


if __name__ == "__main__":
    evaluate_matcher()