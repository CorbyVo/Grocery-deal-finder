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
    # offers_df[offers_df["normalized_name"].isin(shopping_list)]: select the column named "normalized_name",
    # then check if each value in the column inside the shopping_list -> return True / False
    # then keep only the row where it returns True value
    # copy(): copy the filtered DataFrame -> make it safer to work with the result

    # => we get a smaller table containing only thr products the user wants

    matched_offers = offers_df[offers_df["normalized_name"].isin(shopping_list)].copy()

    basket_totals = (
        matched_offers.groupby("store_id")["price"] # group the filter DataFrame by store_id, then look at the prices only
        .sum()                                      # sum the prices in each group
        .reset_index() # when using sum((). mean(), count(), etc after groupby(), the groupby() column become the index of the aggregated result
                       # therefore, we need to reset_index(), to build another index column, and return groupby() to be the normal column
        .rename(columns={"price": "basket_total"})
    )
    return matched_offers, basket_totals

if __name__ == "__main__": # run the code below only if this file is executed directly
    offers_df = load_offers()

    shopping_list = ["milk", "eggs", "pasta"]
    matched_offers, result = compare_basket(shopping_list, offers_df)

    print("Shopping list:", shopping_list)
    print("\nMatched offers:")
    print(matched_offers)
    print("\nBasket totals:")
    print(result)