import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.pipeline import run_pipeline
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Grocery Deal Finder", layout="wide")

st.title("Grocery Deal Finder")
st.write("Compare supermarket offers and get the best store recommendation.")

user_input = st.text_area(
    "Enter your shopping list (one item per line):", value="egg\npasta\nspaghetti"
)

st.subheader("Your location")
user_latitude = st.number_input("Latitude", value=52.5200, format="%.6f")
user_longitude = st.number_input("Longitude", value=13.4050, format="%.6f")

if st.button("Compare"):
    user_shopping_list = [line.strip() for line in user_input.split("\n") if line.strip()]

    result = run_pipeline(user_shopping_list, user_latitude, user_longitude, threshold=0.50)

    st.subheader("1. Matched Products")
    matched_df = pd.DataFrame(result["matched_details"]) # pd.DataFrame(dictionary or list data)
    st.dataframe(matched_df, use_container_width=True)

    st.subheader("2. Unrecognized Products")
    if result["unmatched_user_inputs"]:
        st.warning(
            "These user inputs could not be matched to the product catalog: "
            + ", ".join(result["unmatched_user_inputs"])
        )
    else:
        st.success("All user inputs were recognized.")

    st.subheader("3. Store Comparison")
    if result["store_comparison"] is not None:
        display_column = [
            "store_id",
            "store_name",
            "basket_total",
            "distance_km",
            "requested_items",
            "matched_items",
            "unmatched_items",
        ]
        store_comparison = result["store_comparison"][display_column].copy()
        st.dataframe(store_comparison, use_container_width=True)

        st.subheader("Recommendations")
        st.success(result["message"])

    else:
        st.subheader("Recommendations")
        st.warning("No store comparison available because no reliable matches were found.")

