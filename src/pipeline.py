from src.matcher import ProductMatcher
from src.recommend import recommend_store


def run_pipeline(user_shopping_list, user_latitude, user_longitude, threshold = 0.50):
    """
    Full pipeline:
    1. Match raw user input to normalize product names
    2. Keep unmatched user inputs separately
    3. Recommend to best store
    """
    matcher = ProductMatcher()

    user_shopping_list = list(set(user_shopping_list))
    original_request_count = len(user_shopping_list)
    matching_details = []  # list of normalized products with their info
    unmatched_user_inputs = []

    for item in user_shopping_list:
        best_match, best_score = matcher.match_product(item, threshold = threshold)
        matching_details.append(
            {
                "user_input": item,
                "matched_product": best_match,
                "similarity_score": round(best_score, 4) if best_score else None
            }
        )
        """for 1st version: keep clean_match_products [] unique, will update the quantity in version 2"""
        if best_match is None:
            unmatched_user_inputs.append(item)
    matched_details = [row for row in matching_details if row["matched_product"] is not None]

    if not matched_details:
        return {
            "matched_details": matching_details,
            "unmatched_user_inputs": unmatched_user_inputs,
            "store_comparison": None,
            "cheapest_store": None,
            "nearest_store": None,
            "message": "No reliable product matches were found."
        }

    matched_offers, basket_summary,cheapest_store, nearest_store, message = recommend_store(matched_details,
                                                                                original_request_count, unmatched_user_inputs, user_latitude, user_longitude)

    return {
        "matched_details": matched_details,
        "unmatched_user_inputs": unmatched_user_inputs,
        "store_comparison": basket_summary,
        "cheapest_store": cheapest_store,
        "nearest_store": nearest_store,
        "message": message
    }

if __name__ == "__main__":
    user_shopping_list = ["fish", "chicken drum stick","whole milk", "10 eggs", "spaghetti", "apples"]
    user_latitude = 52.5200
    user_longitude = 13.4050
    result = run_pipeline(user_shopping_list, user_latitude, user_longitude, threshold = 0.5)

    print("\nShopping list:", user_shopping_list)

    print("\nMatched result:")
    for row in result ["matched_details"]:
        print(row)

    print("\nUnmatched user inputs:", result["unmatched_user_inputs"])

    if result ["store_comparison"] is not None:
        print("\nStore comparison:")
        print(
            result["store_comparison"][
                ["store_id", "store_name", "basket_total", "matched_items", "requested_items", "matched_items_list", "unmatched_items", "is_complete", "distance_km"]
            ]
        )
    print("\nRecommendation message:")
    print(result["message"])