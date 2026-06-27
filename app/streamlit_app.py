import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import re

from src.project_rag import ProjectRetriever
from src.pipeline import run_pipeline
import pandas as pd
import streamlit as st

def clean_chunk_for_chat(chunk):
    chunk = chunk.strip()

    # remove markdown horizontal rules
    chunk = re.sub(r"^\s*---+\s*$", "", chunk, flags=re.MULTILINE)

    # remove markdown headings like # ## ### at line starts
    chunk = re.sub(r"^\s*#+\s*", "", chunk, flags=re.MULTILINE)

    # remove headings that appear after separators, like --- ## Week 1
    chunk = re.sub(r"---+\s*#+\s*", "", chunk)

    # remove checklist markers like - [x] or - [ ]
    chunk = re.sub(r"[-*]\s*\[[xX ]\]\s*", "", chunk)

    # remove bullet markers at line starts
    chunk = re.sub(r"^\s*[-*]\s+", "", chunk, flags=re.MULTILINE)

    # remove standalone numbered heading fragments like "12."
    chunk = re.sub(r"^\s*\d+\.\s*$", "", chunk, flags=re.MULTILINE)

    # remove leading numbered section titles like "12. What recruiters should see"
    chunk = re.sub(r"^\s*\d+\.\s+", "", chunk, flags=re.MULTILINE)

    # replace line breaks with spaces
    chunk = chunk.replace("\n", " ")

    # collapse repeated spaces
    chunk = re.sub(r"\s+", " ", chunk)

    return chunk.strip()

def build_project_chat_answer(question, results, visible_k=1, max_chars_per_chunk=260):
    visible_results = results[:visible_k]
    answer_points = []

    for result in visible_results:
        chunk = clean_chunk_for_chat(result["chunk"])
        chunk = re.sub(r"^[A-Z][^\n?]{0,120}\?\s*", "", chunk)

        if len(chunk) < 20 or re.fullmatch(r"[\d.\- ]+", chunk):
            continue

        if len(chunk) > max_chars_per_chunk:
            chunk = chunk[:max_chars_per_chunk].rsplit(" ", 1)[0] + "..."

        answer_points.append(chunk)

    if not answer_points:
        answer_points.append("I found related project notes, but they need cleaner formatting before summarizing well.")

    source_names = sorted({result["source"] for result in visible_results})

    answer_text = (
        f"Here’s what I found about **{question.strip()}**:\n\n"
        + "\n\n".join(answer_points)
        + "\n\n"
        + f"**Main source used:** {', '.join(source_names)}"
    )

    return answer_text

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
        store_comparison = result["store_comparison"][display_column].copy()

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
        answer_text = build_project_chat_answer(project_question, results, visible_k=1)

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