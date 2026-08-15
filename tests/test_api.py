import pandas as pd
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# FastAPI endpoint test
def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Grocery Deal Finder API is running"


def test_stores_nearby_endpoint(monkeypatch):
    fake_stores = pd.DataFrame(
        [
            {
                "store_id": 1,
                "store_name": "REWE Test",
                "store_latitude": 47.8560,
                "store_longitude": 12.1220,
            },
            {
                "store_id": 2,
                "store_name": "Lidl Test",
                "store_latitude": 47.8500,
                "store_longitude": 12.1300,
            },
        ]
    )

    def fake_load_stores():
        return fake_stores.copy()

    monkeypatch.setattr("api.main.load_stores", fake_load_stores)

    response = client.post(
        "/stores/nearby",
        json={
            "lat": 47.8560,
            "lon": 12.1220
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["store_name"] == "REWE Test"
    assert "distance_km" in data[0]

# /compare endpoint test
def test_compare_endpoint(monkeypatch):
    fake_store_comparison = pd.DataFrame(
        [
            {
                "store_id": 1,
                "store_name": "REWE Test",
                "basket_total": 4.50,
                "distance_km": 1.2,
                "requested_items": 2,
                "matched_items": 2,
                "unmatched_items": [],
            }
        ]
    )

    fake_result = {
        "matched_details": [
            {
                "user_input": "egg",
                "matched_product": "eggs",
                "similarity_score": 0.95,
                "confidence": "high",
                "method": "alias_exact",
            }
        ],
        "unmatched_user_inputs": [],
        "store_comparison": fake_store_comparison,
        "message": "Best store is REWE Test."
    }

    def fake_run_pipeline(shopping_list, latitude, longitude, threshold=0.5):
        return fake_result

    monkeypatch.setattr("api.main.run_pipeline", fake_run_pipeline)

    response = client.post(
        "/compare",
        json={
            "shopping_list": ["egg"],
            "latitude": 47.8560,
            "longitude": 12.1220,
            "threshold": 0.5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["matched_details"][0]["matched_product"] == "eggs"
    assert data["store_comparison"][0]["store_name"] == "REWE Test"
    assert data["message"] == "Best store is REWE Test."