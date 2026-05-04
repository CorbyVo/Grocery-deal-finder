from src.load_data import load_offers, load_stores
import pandas as pd

def compare_basket(normalized_shopping_list, num_of_original_shopping_items, offers_df, stores_df,):
    """
    Compare basket total across stores for a given shopping list and check basket completeness.
    Parameters:
        normalized_shopping_list (list[str]): list of normalized product names
        offers_df (pd.DataFrame): dataframe containing offers)
    Return:
        match_offers (pd.DataFrame)
        basket_summary (pd.DataFrame)
    """
    # offers_df[offers_df["normalized_name"].isin(normalized_shopping_list)]: select the column named "normalized_name",
    # then check if each value in the column inside the shopping_list -> return True / False
    # then keep only the row where it returns True value
    # copy(): copy the filtered DataFrame -> make it safer to work with the result

    # => we get a smaller table containing only the products the user wants
    normalized_shopping_set = set(normalized_shopping_list) # set() is designed for jast membership checks
    matched_offers = offers_df[offers_df["normalized_name"].isin(normalized_shopping_set)].copy()

    basket_summary = (
        matched_offers.groupby("store_id")
        .agg( basket_total = ("price", "sum"), matched_items = ("normalized_name", "nunique"))
        .reset_index()
    )

    basket_summary["requested_items"] = num_of_original_shopping_items
    basket_summary["is_complete"] = (basket_summary["matched_items"] == basket_summary["requested_items"])
    basket_summary = basket_summary.merge(stores_df, on="store_id", how="left")

    return matched_offers, basket_summary

if __name__ == "__main__":
    offers_df = load_offers()
    stores_df = load_stores()

    normalized_shopping_list = ["milk", "eggs", "pasta", "apples"]
    num_item = 4
    matched_offers, summary = compare_basket(normalized_shopping_list, num_item, offers_df, stores_df)

    print(" Normalized shopping list:", normalized_shopping_list)
    print("\nMatched offers:")
    print(matched_offers)
    print("\nBasket summary:")
    print(summary.T)