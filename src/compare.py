from src.load_data import load_offers, load_stores
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

def compare_basket(matched_details, num_of_original_shopping_items, unmatched_user_inputs, offers_df, stores_df,):
    """
    Compare basket total across stores for a
        given details of normalized items and
        check basket completeness.
    Parameters:
        matched_details (list[dict]): list of details of normalized items
        num_of_original_shopping_items (int): number of original shopping

        offers_df (pd.DataFrame): offer data
        stores_df (pd.DataFrame): stores data
    Return:
        match_offers (pd.DataFrame)
        basket_summary (pd.DataFrame)
    """
    # offers_df[offers_df["normalized_name"].isin(normalized_shopping_list)]: select the column named "normalized_name",
    # then check if each value in the column inside the shopping_list -> return True / False
    # then keep only the row where it returns True value
    # copy(): copy the filtered DataFrame -> make it safer to work with the result

    # => we get a smaller table containing only the products the user wants
    normalized_shopping_list = [row["matched_product"] for row in matched_details]
    normalized_shopping_set = set(normalized_shopping_list) # set() is designed for jast membership checks
    matched_offers_df = offers_df[offers_df["normalized_name"].isin(normalized_shopping_set)].copy()

    basket_summary_rows = []

    for _, store_row in stores_df.iterrows():
        store_id = store_row["store_id"]
        store_name = store_row["store_name"]
        store_latitude = store_row["store_latitude"]
        store_longitude = store_row["store_longitude"]

        matched_offers_per_store_df = matched_offers_df[matched_offers_df["store_id"] == store_id]
        store_matched_offers_per_store_names = set(matched_offers_per_store_df["normalized_name"].tolist())

        basket_total = matched_offers_per_store_df["price"].sum()

        covered_user_inputs = []
        uncovered_user_inputs = []

        for row in matched_details:
            original_input = row["user_input"]
            matched_input = row["matched_product"]

            if matched_input in store_matched_offers_per_store_names:
                covered_user_inputs.append(original_input)
            else:
                uncovered_user_inputs.append(original_input)

        all_unmatched_items = sorted(set(uncovered_user_inputs + unmatched_user_inputs))

        basket_summary_rows.append(
            {
                "store_id": store_id,
                "store_name": store_name,
                "basket_total": basket_total,
                "is_complete": len(all_unmatched_items) == 0,
                "requested_items": num_of_original_shopping_items,
                "matched_items": len(covered_user_inputs),
                "unmatched_items": all_unmatched_items,
                "store_latitude": store_latitude,
                "store_longitude": store_longitude,
            }
        )

    basket_summary = pd.DataFrame(basket_summary_rows)

    return matched_offers_df, basket_summary

if __name__ == "__main__":
    offers_df = load_offers()
    stores_df = load_stores()

    normalized_shopping_list = ["milk", "eggs", "pasta", "apples", "shrimp"]
    num_item = len(set(normalized_shopping_list))
    matched_offers, basket_summary = compare_basket(normalized_shopping_list, num_item, offers_df, stores_df)

    print(" Normalized shopping list:", normalized_shopping_list)
    print("\nMatched offers:")
    print(matched_offers)
    print("\nBasket summary:")
    print(basket_summary[["store_id", "store name", "basket_total", "matched_items", "requested_items", "matched_items_list", "unmatched_items", "is_complete"]])