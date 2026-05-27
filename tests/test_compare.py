import pandas as pd
from src.compare import compare_basket

def test_many_to_one_normalization_still_counts_as_complete():
    matched_details = [
        {"user_input": "egg", "matched_product": "eggs", "similarity_score": 0.91},
        {"user_input": "pasta", "matched_product": "pasta", "similarity_score": 0.95},
        {"user_input": "spaghetti", "matched_product": "pasta", "similarity_score": 0.89},
    ]

    num_of_original_shopping_items = 3
    unmatched_user_inputs = []

    offers_df = pd.DataFrame(
        [
            {"store_id": 1, "normalized_name": "eggs", "price": 2.09},
            {"store_id": 1, "normalized_name": "pasta", "price": 0.79},
        ]
    )

    stores_df = pd.DataFrame(
        [
            {
                "store_id": 1,
                "store_name": "Lidl",
                "store_latitude": 52.5200,
                "store_longitude": 13.4050,
            }
        ]
    )

    matched_offers, basket_summary = compare_basket(matched_details = matched_details,
                                                    num_of_original_shopping_items = num_of_original_shopping_items,
                                                    unmatched_user_inputs = unmatched_user_inputs,
                                                    offers_df = offers_df,
                                                    stores_df = stores_df,)

    row = basket_summary.iloc[0]

    assert row["matched_items"] == 3
    assert row["requested_items"] == 3
    assert row["is_complete"] == True
    assert row["unmatched_items"] == []