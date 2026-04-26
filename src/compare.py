from rapidfuzz.distance.DamerauLevenshtein_py import normalized_distance

from load_data import load_offers
import pandas as pd

def compare_basket(normalized_shopping_list, offers_df):
    """
    Compare basket total across stores for a given shopping list and check basket completeness.
    Parameters:
        shopping_list (list[str]): list of normalized product names
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
    basket_summary = pd.DataFrame()
    matched_offers = offers_df[offers_df["normalized_name"].isin(normalized_shopping_set)].copy()

    basket_summary = (
        matched_offers.groupby("store_id") # group the filter DataFrame by store_id
        .agg( basket_total = ("price", "sum"), # look for the "price" column, add all prices together, store the result in new column named "basket_total"
              matched_items = ("normalized_name", "nunique")) # look at "normalized_name" column, count how many unique product name exist, store the result in the new column named matched_items
        .reset_index() # when using sum((). mean(), count(), etc after groupby(), the groupby() column become the index of the aggregated result
                       # therefore, we need to reset_index(), to build another index column, and return groupby() to be the normal column
    )

    basket_summary["requested_items"] = len(normalized_shopping_set)
    basket_summary["is_complete"] = (basket_summary["matched_items"] == basket_summary["requested_items"])

    return matched_offers, basket_summary

if __name__ == "__main__": # run the code below only if this file is executed directly
    offers_df = load_offers()

    normalized_shopping_list = ["milk", "eggs", "pasta", "apples"]
    matched_offers, summary = compare_basket(normalized_shopping_list, offers_df)

    print(" Normalized shopping list:", normalized_shopping_list)
    print("\nMatched offers:")
    print(matched_offers)
    print("\nBasket summary:")
    print(summary)