from pathlib import Path
import sys
from typing import List, Any

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

# Allow importing from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.distance import calculate_distance_km
from src.pipeline import run_pipeline
from src.ocr_reader import extract_text_from_image, parse_shopping_items
from src.llm_cleaner import clean_items_with_llm

app = FastAPI(
    title="Grocery Deal Finder API",
    description="API for store locations and location-aware grocery recommendations.",
    version="1.0.0",
)

DATA_PATH = PROJECT_ROOT / "data" / "stores.csv"


class UserLocation(BaseModel):
    lat: float = Field(..., example=47.8560)
    lon: float = Field(..., example=12.1220)


class CompareRequest(BaseModel):
    shopping_list: List[str] = Field(..., example=["egg", "pasta", "spaghetti"])
    latitude: float = Field(..., example=47.8560)
    longitude: float = Field(..., example=12.1220)
    threshold: float = Field(default=0.50, example=0.50)


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