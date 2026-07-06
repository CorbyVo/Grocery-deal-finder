import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import re
import requests
from src.project_rag import ProjectRetriever
import pandas as pd
import streamlit as st

API_COMPARE_URL = "http://127.0.0.1:8000/compare"



def build_project_chat_answer(question, results):
    if not results:
        return "No relevant project information was found."
    best_result = results[0]
    chunk = best_result["chunk"].strip()
    # If the best source is the FAQ, use it almost directly
    if best_result["source"] == "project_faq.md":
        chunk = re.sub(r"^[A-Z][^\n?]{0,120}\?\s*", "", chunk).strip()
        return chunk
    # Light cleanup for non-FAQ sources
    chunk = chunk.replace("\n", " ")
    chunk = re.sub(r"\s+", " ", chunk).strip()
    return chunk

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
    api_payload = {
        "shopping_list": user_shopping_list,
        "latitude": user_latitude,
        "longitude": user_longitude,
        "threshold": 0.50
    }
    try:
        response = requests.post(API_COMPARE_URL, json=api_payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.ConnectionError:
        st.error("FastAPI backend is not running. Start it with: uvicorn api.main:app --reload")
        st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        st.stop()

    st.subheader("1. Matched Products")
    matched_df = pd.DataFrame(result["matched_details"])
    user_view_df = matched_df[["user_input", "matched_product"]].copy()
    st.dataframe(user_view_df, use_container_width=True)
    with st.expander("Show AI matching details"):
        ai_view_df = matched_df[
            ["user_input", "matched_product", "similarity_score", "confidence", "method"]
        ].copy()
        st.dataframe(ai_view_df, use_container_width=True)

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
        store_comparison = pd.DataFrame(result["store_comparison"])
        store_comparison = store_comparison[display_column].copy()
        store_comparison["unmatched_items"] = store_comparison["unmatched_items"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) and len(x) > 0 else "None"
        )
        store_comparison["basket_total"] = store_comparison["basket_total"].apply(
            lambda x: f"€{x:.2f}"
        )
        store_comparison["distance_km"] = store_comparison["distance_km"].round(2)
        store_comparison = store_comparison.rename(
            columns={
                "store_id": "Store ID",
                "store_name": "Store",
                "basket_total": "Basket Total",
                "distance_km": "Distance (km)",
                "requested_items": "Requested Items",
                "matched_items": "Matched Items",
                "unmatched_items": "Unmatched Items",
            }
        )
        st.dataframe(store_comparison, use_container_width=True)

        st.subheader("Recommendations")
        st.success(result["message"])
    else:
        st.subheader("Recommendations")
        st.warning("No store comparison available because no reliable matches were found.")

st.divider()

st.subheader("Project Q&A Assistant")
st.write("Ask about this project, how it works, its limitations, or next steps.")

if "project_retriever" not in st.session_state:
    st.session_state.project_retriever = ProjectRetriever()

if "project_chat_history" not in st.session_state:
    st.session_state.project_chat_history = []

for idx, message in enumerate(st.session_state.project_chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and "sources" in message:
            with st.expander(f"Retrieved Sources for answer {idx + 1}", expanded=False):
                for i, result in enumerate(message["sources"], start=1):
                    st.write(f"**Chunk {i}**")
                    st.write(f"Source: {result['source']}")
                    st.write(f"Similarity score: {result['score']}")
                    st.write("---")

project_question = st.chat_input("Ask a question about this project")

if project_question:
    st.session_state.project_chat_history.append(
        {
            "role": "user",
            "content": project_question
        }
    )

    results = st.session_state.project_retriever.retrieve(project_question, top_k=5)

    if results:
        answer_text = build_project_chat_answer(project_question, results)
        st.session_state.project_chat_history.append(
            {
                "role": "assistant",
                "content": answer_text,
                "sources": results
            }
        )
    else:
        st.session_state.project_chat_history.append(
            {
                "role": "assistant",
                "content": "No relevant project information was found."
            }
        )
    st.rerun()