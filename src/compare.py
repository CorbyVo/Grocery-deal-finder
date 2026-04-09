import pandas as pd
from load_data import load_offers

def compare_basket(shopping_list, offers_df):
    """
    Compare basket total across stores for a given shopping list.
    :param
        shopping_list (list[str]): list of normalized product names
        offers_df (pd.DataFrame): dataframe containing offers)
    :return:
        pd.DataFrame: dataFrame: basket total per store
    """
    matched_offers = offers_df[offers_df["normalized_name"].isin(shopping_list)].copy()

    basket_totals = (
        matched_offers.groupby("store_id")["price"]
        .sum()
        .reset_index()
        .rename(columns={"price": "basket_total"})
    )
    return matched_offers, basket_totals

if __name__ == "__main__":
    offers_df = load_offers()

    shopping_list = ["milk", "eggs", "pasta"]
    matched_offers, result = compare_basket(shopping_list, offers_df)

    print("Shopping list:", shopping_list)
    print("\nMatched offers:")
    print(matched_offers)
    print("\nBasket totals:")
    print(result)