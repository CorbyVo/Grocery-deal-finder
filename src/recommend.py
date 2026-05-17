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
        candidate_stores = complete_stores
        cheapest_store_row = complete_stores.sort_values("basket_total").iloc[0]
        note = "Only complete baskets are considered."

    return cheapest_store_row, note, candidate_stores


def build_recommendation_message(cheapest_store_row, nearest_store_row, note):
    cheapest_store_name = cheapest_store_row["store_name"]
    cheapest_store_price = cheapest_store_row["basket_total"]
    cheapest_store_distance = cheapest_store_row["distance_km"]

    nearest_store_name = nearest_store_row["store_name"]
    nearest_store_price = nearest_store_row["basket_total"]
    nearest_store_distance = nearest_store_row["distance_km"]

    if cheapest_store_name == nearest_store_name:
        message = (f"{note}"
                   f"\nThe best store is {cheapest_store_name} for €{cheapest_store_price:.2f}"
                   f" with distance of {cheapest_store_distance:.2f} km.")
    else:
        price_gap = abs(cheapest_store_price - nearest_store_price)
        distance_gap = abs(cheapest_store_distance - nearest_store_distance)
        message = (f"{note}\n\n"
                   f"There is a tradeoff:\n"
                   f"- Cheapest store: {cheapest_store_name} (€{cheapest_store_price:.2f}, {cheapest_store_distance:.2f} km)\n"
                   f"- Nearest store: {nearest_store_name} (€{nearest_store_price:.2f}, {nearest_store_distance:.2f} km)\n\n"
                   f"{cheapest_store_name} saves you €{price_gap:.2f}, while {nearest_store_name} is closer by {distance_gap:.2f} km.\n"
                   f"Feel free to make your decision which meets your demand best!"
                   )

    return message


def recommend_store(matched_details, num_of_original_shopping_items, unmatched_user_inputs, user_latitude, user_longitude):
    """
    give the recommendation based on 'cheapest store' and 'nearest store'
    """
    stores_df = load_stores()
    offers_df = load_offers()

    matched_offers, basket_summary = compare_basket(matched_details, num_of_original_shopping_items, unmatched_user_inputs, offers_df, stores_df)

    basket_summary["distance_km"] = basket_summary.apply(
        lambda row: calculate_distance_km(user_latitude, user_longitude, row["store_latitude"], row["store_longitude"]), axis=1)

    cheapest_store_row, note, candidate_stores = find_cheapest_store(basket_summary)

    nearest_store_row = find_nearest_store(candidate_stores)

    message = build_recommendation_message(cheapest_store_row, nearest_store_row, note)

    return matched_offers, basket_summary,cheapest_store_row, nearest_store_row, message



if __name__ == "__main__":
    normalized_shopping_list = ["milk", "eggs", "pasta", "apples"]
    num_item = len(set(normalized_shopping_list))
    user_latitude = 52.5200
    user_longitude = 13.4050
    match_offers, basket_summary, cheapest_store_row, nearest_store_row, message = recommend_store(normalized_shopping_list, num_item, user_latitude, user_longitude)

    print("\nShopping list:", normalized_shopping_list)
    print("\nMatched offers:")
    print(match_offers)

    print("\nStore comparison:")
    print(basket_summary[["store_id", "store_name", "basket_total", "matched_items", "requested_items", "matched_items_list", "unmatched_items", "is_complete", "distance_km"]])

    print("\nRecommendations:")
    print(message)