from geopy.distance import geodesic
from src.load_data import load_stores, load_offers
from src.compare import compare_basket
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


def calculate_distance_km(user_latitude, user_longitude, store_latitude, store_longitude):
    """
        Calculate distance in kilometers between user and store coordinates.
    """
    return geodesic((user_latitude, user_longitude ), (store_latitude, store_longitude)).km


def find_nearest_store( candidate_stores):
    nearest_store_row = candidate_stores.sort_values("distance_km").iloc[0]

    return nearest_store_row


def find_cheapest_store(basket_summary):
    complete_stores = basket_summary[basket_summary["is_complete"] == True].copy()

    if complete_stores.empty:
        candidate_stores = basket_summary.copy()
        cheapest_store_row = basket_summary.sort_values(by=["matched_items", "basket_total"], ascending=[False, True]).iloc[0]
        note = "No store has all requested items, so partial baskets are considered."
    else:
        candidate_stores = complete_stores.copy()
        cheapest_store_row = complete_stores.sort_values("basket_total").iloc[0]
        note = "Only complete baskets are considered."

    return cheapest_store_row, note, candidate_stores


def recommend_store(normalized_shopping_list, num_of_original_shopping_items, user_latitude, user_longitude):
    """
    give the recommendation based on 'cheapest store' and 'nearest store'
    """
    stores_df = load_stores()
    offers_df = load_offers()

    matched_offers, basket_summary = compare_basket(normalized_shopping_list, num_of_original_shopping_items, offers_df, stores_df)
    basket_summary["distance_km"] = basket_summary.apply(
        lambda row: calculate_distance_km(user_latitude, user_longitude, row["store_latitude"], row["store_longitude"]), axis=1)

    cheapest_store_row, note, candidate_stores = find_cheapest_store(basket_summary)
    nearest_store_row = find_nearest_store(candidate_stores)

    if cheapest_store_row["store name"] == nearest_store_row["store name"]:
        message = (f"{note}"
                   f"\nThe best store is {cheapest_store_row['store name']}"
                   f" with {cheapest_store_row['matched_items']} matched items for €{cheapest_store_row['basket_total']:.2f},"
                   f" \nwith the distance of {cheapest_store_row['distance_km']:.2f} km from your location")
    else:
        message = (f"{note}"
                  f"\nThe cheapest store is {cheapest_store_row['store name']} with {cheapest_store_row['matched_items']} matched items for €{cheapest_store_row['basket_total']:.2f}."
                  f"\nThe nearest store is {nearest_store_row['store name']} with distance of {nearest_store_row['distance_km']:.2f} km."
                  )

    return matched_offers, basket_summary,cheapest_store_row, nearest_store_row, message

if __name__ == "__main__":
    normalized_shopping_list = ["milk", "eggs", "pasta", "apples"]
    num_item = 4
    user_latitude = 52.5200
    user_longitude = 13.4050
    match_offers, basket_summary, cheapest_store_row, nearest_store_row, message = recommend_store(normalized_shopping_list, num_item, user_latitude, user_longitude)

    print("\nShopping list:", normalized_shopping_list)
    print("\nMatched offers:")
    print(match_offers)

    print("\nStore comparison:")
    print(basket_summary[["store_id", "store name", "basket_total", "matched_items", "requested_items", "is_complete", "distance_km"]])

    print("\nRecommendations:")
    print(message)