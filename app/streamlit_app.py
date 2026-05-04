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

user_latitude = st.number_input(
    "Latitude",
    value=52.5200,
    format="%.6f"
)
user_longitude = st.number_input(
    "Longitude",
    value=13.4050,
    format="%.6f"
)

if st.button("Compare"):
    user_shopping_list = [line.strip() for line in user_input.split("\n") if line.strip()]

    result = run_pipeline(user_shopping_list, user_latitude, user_longitude, threshold=0.50)

    st.subheader("Matched Products")
    matched_df = pd.DataFrame(result["matched_details"]) # pd.DataFrame(dictionary or list data)
    st.dataframe(matched_df, use_container_width=True)



    if result["store_comparison"] is not None:
        st.subheader("Recommendations")
        st.success(result["message"])
        st.subheader("Store Comparison")
        st.dataframe(result["store_comparison"], use_container_width=True)
    else:
        st.subheader("Recommendations")
        st.warning("No store comparison available because no reliable matches were found.")

