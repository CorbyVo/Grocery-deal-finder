from src.load_data import load_stores, load_offers
from src.compare import compare_basket


def recommend_cheapest_store(shopping_list):
    stores_df = load_stores()
    offers_df = load_offers()

    matched_offers, basket_summary = compare_basket(shopping_list, offers_df)

    merged_basket = basket_summary.merge(stores_df, on = "store_id", how = "left") # keep all row from the left table (basket_totals),
                                                                                  # find matching rows in the right table (stores_df)
                                                                                  # and attach the other store columns
    complete_store = merged_basket[merged_basket["is_complete"] == True].copy()

    if not complete_store.empty:
        best_store = complete_store.sort_values("basket_total").iloc[0]
        message = (
            f"The best complete store is {best_store['name']}"
            f" for €{best_store['basket_total']:.2f}."
        )
    else:
        best_store = merged_basket.sort_values(
            by=["matched_items", "basket_total"], # sort by 2 columns
            ascending=[False, True]).iloc[0] # matched_items : descending -> bigger first
                                             # basket_total: ascending -> smaller first
        # Choose the store that has the most requested items, and if two stores tie, choose the  cheaper one
        message = (
            f"No store has all requested items."
            f" The best partial option is {best_store['name']} "
            f"with {best_store['matched_items']} matched items "
            f"for €{best_store['basket_total']:.2f}."
        )
      # sort store from cheapest to most expensive, then pick the 1st one

    return matched_offers, merged_basket,best_store, message

if __name__ == "__main__":
    shopping_list = ["milk", "eggs", "pasta", "apples"]
    match_offers, merged_basket, best_store, message = recommend_cheapest_store(shopping_list)

    print("\nShopping list:", shopping_list)
    print("\nMatched offers:")
    print(match_offers)

    print("\nStore comparison:")
    print(merged_basket[["store_id", "name", "basket_total", "matched_items", "requested_items", "is_complete"]])

    print("\nRecommendations:")
    print(message)