from pathlib import Path
import sys
import re
from typing import List, Any

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Allow importing from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.distance import calculate_distance_km
from src.pipeline import run_pipeline
from src.ocr_reader import extract_text_from_image, parse_shopping_items
from src.llm_cleaner import clean_items_with_llm
from src.project_rag import ProjectRetriever

app = FastAPI(
    title="Grocery Deal Finder API",
    description="API for store locations and location-aware grocery recommendations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = PROJECT_ROOT / "data" / "stores.csv"
project_retriever = ProjectRetriever()

class UserLocation(BaseModel):
    lat: float = Field(..., json_schema_extra= {"example" : 47.8560})
    lon: float = Field(..., json_schema_extra= {"example": 12.1220})


class CompareRequest(BaseModel):
    shopping_list: List[str] = Field(..., json_schema_extra= {"example":["egg", "pasta", "spaghetti"]})
    latitude: float = Field(..., json_schema_extra={ "example":47.8560})
    longitude: float = Field(...,json_schema_extra={"example":12.1220})
    threshold: float = Field(default=0.50,json_schema_extra={"example": 0.50})

class ProjectChatRequest(BaseModel):
    question: str = Field(..., json_schema_extra={"example": "What does this project do?"})


def load_stores():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="stores.csv not found")
    return pd.read_csv(DATA_PATH)


def make_json_safe(value: Any):
    """
    Convert pandas / numpy objects into normal Python objects
    so FastAPI can return them as JSON.
    """
    if isinstance(value, pd.DataFrame):
        return value.to_dict(orient="records")
    if isinstance(value, pd.Series):
        return value.to_dict()
    if isinstance(value, dict):
        return {key: make_json_safe(val) for key, val in value.items()}
    if isinstance(value, list):
        return [make_json_safe(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value

def clean_project_chunk(chunk: str) -> str:
    chunk = chunk.strip()

    chunk = re.sub(r"^\s*---+\s*$", "", chunk, flags=re.MULTILINE)
    chunk = re.sub(r"^\s*#+\s*", "", chunk, flags=re.MULTILINE)
    chunk = re.sub(r"---+\s*#+\s*", "", chunk)
    chunk = re.sub(r"[-*]\s*\[[xX ]\]\s*", "", chunk)
    chunk = re.sub(r"^\s*[-*]\s+", "", chunk, flags=re.MULTILINE)
    chunk = re.sub(r"^\s*\d+\.\s*$", "", chunk, flags=re.MULTILINE)
    chunk = re.sub(r"^\s*\d+\.\s+", "", chunk, flags=re.MULTILINE)
    chunk = re.sub(r"^[A-Z][^\n?]{0,120}\?\s*", "", chunk)
    chunk = chunk.replace("\n", " ")
    chunk = re.sub(r"\s+", " ", chunk)

    return chunk.strip()


@app.get("/")
def root():
    return {
        "message": "Grocery Deal Finder API is running",
        "docs": "/docs"
    }


@app.get("/stores")
def get_stores():
    stores = load_stores()
    return stores.to_dict(orient="records")


@app.post("/stores/nearby")
def get_nearby_stores(user_location: UserLocation):
    stores = load_stores()
    stores["distance_km"] = stores.apply(
        lambda row: calculate_distance_km(
            user_location.lat,
            user_location.lon,
            row["store_latitude"],
            row["store_longitude"]
        ), axis=1
    )
    stores["distance_km"] = stores["distance_km"].round(2)
    stores = stores.sort_values("distance_km")
    return stores.to_dict(orient="records")


@app.post("/stores/nearest")
def get_nearest_store(user_location: UserLocation):
    stores = load_stores()
    stores["distance_km"] = stores.apply(
        lambda row: calculate_distance_km(
            user_location.lat,
            user_location.lon,
            row["store_latitude"],
            row["store_longitude"]
        ),axis=1
    )
    stores["distance_km"] = stores["distance_km"].round(2)
    nearest_store = stores.sort_values("distance_km").iloc[0]
    return nearest_store.to_dict()


@app.post("/compare")
def compare_grocery_deals(request: CompareRequest):
    result = run_pipeline(
        request.shopping_list,
        request.latitude,
        request.longitude,
        threshold=request.threshold
    )
    return make_json_safe(result)


@app.post("/ocr/shopping-list")
async def ocr_shopping_list(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )
    image_bytes = await file.read()
    raw_text = extract_text_from_image(image_bytes)
    raw_items = parse_shopping_items(raw_text)
    cleaned_items = clean_items_with_llm(raw_text, raw_items)
    return {
        "filename": file.filename,
        "raw_text": raw_text,
        "raw_items": raw_items,
        "cleaned_items": cleaned_items
    }


@app.post("/project-chat")
def project_chat(request: ProjectChatRequest):
    results = project_retriever.retrieve(request.question, top_k=3)
    if not results:
        return {
            "answer": "No relevant project information was found.",
            "sources": []
        }
    best_chunk = clean_project_chunk(results[0]["chunk"])
    if len(best_chunk) > 500:
        best_chunk = best_chunk[:500].rsplit(" ", 1)[0] + "..."
    sources = [
        {
            "source": result["source"],
            "score": result["score"]
        }
        for result in results
    ]
    return {
        "answer": best_chunk,
        "sources": sources
    }