from matcher import ProductMatcher
from recommend import recommend_cheapest_store


def run_pipeline(user_shopping_list, threshold = 0.50):
    """
    Full pipeline:
    1. Match raw user input to normalize product names
    2. Recommend to best store
    """

    matcher = ProductMatcher()
    matched_details = []     # match the user list with normalized list -> list of normalized products with their info
    clean_matched_products = []    # remove None, bad match, duplicates from matched_products

    for item in user_shopping_list:
        best_match, best_score = matcher.match_product(item, threshold = threshold)
        matched_details.append(
            {
                "user_input": item,
                "matched_product": best_match,
                "similarity_score": round(best_score, 4)
            }
        )
        """for 1st version: keep clea_match_products [] unique, will update the quantity in version 2"""
        if best_match is not None and best_match not in clean_matched_products: # remove None and duplicates
            clean_matched_products.append(best_match)

    if not clean_matched_products:
        return {
            "matched_details": matched_details,
            "store_comparison": None,
            "best_store": None,
            "message": "No reliable product matches were found."
        }
    matched_offers, comparison_result_df, best_store, message = recommend_cheapest_store(clean_matched_products)
    return {
        "matched_details": matched_details,
        "store_comparison": comparison_result_df,
        "best_store": best_store,
        "message": message
    }

if __name__ == "__main__":
    user_shopping_list = ["whole milk", "10 eggs", "spaghetti","fish", "chicken drum stick"]
    result = run_pipeline(user_shopping_list, threshold = 0.5)

    print("Matched result:")
    for row in result ["matched_details"]:
        print(row)

    if result ["store_comparison"] is not None:
        print("\nStore comparison:")
        print(
            result["store_comparison"][
                ["store_id", "name", "basket_total", "matched_items", "requested_items", "is_complete"]
            ]
        )
    print("\nRecommendation message:")
    print(result["message"])