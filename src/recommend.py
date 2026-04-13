from src.load_data import load_stores, load_offers
from src.compare import compare_basket


def recommend_cheapest_store(shopping_list):
    stores_df = load_stores()
    offers_df = load_offers()

    matched_offers, basket_totals = compare_basket(shopping_list, offers_df)

    merged_result = basket_totals.merge(stores_df, on = "store_id", how = "left") # keep all row from the left table (basket_totals),
                                                                                  # find matching rows in the right table (stores_df)
                                                                                  # and attach the other store columns
    cheapest_store = merged_result.sort_values("basket_total").iloc[0] # sort store from cheapest to most expensive, then pick the 1st one

    return matched_offers, merged_result, cheapest_store

if __name__ == "__main__":
    shopping_list = ["milk", "eggs", "pasta"]
    match_offers, full_result, cheapest = recommend_cheapest_store(shopping_list)

    print("Shopping list:", shopping_list)
    print("\nMatched offers:")
    print(match_offers)

    print("\nBasket totals with store info:")
    print(full_result[["store_id", "name", "basket_total"]])

    print("\nRecommendations:")
    print(
        f"The cheapest store is {cheapest['name']}"
        f" with a basket total of €{cheapest['basket_total']:.2f}."
    )