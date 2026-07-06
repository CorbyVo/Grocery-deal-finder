# Grocery Deal Finder

An AI-assisted prototype that helps students or budget-conscious consumers in Germany compare supermarket offers and find the best nearby store based on price and distance.

## Problem
Buyers often need to check multiple supermarket flyers and apps to find the best discounts. This takes time and makes it harder to save money.

---

## Project Goal
Build a simple app that:
- compares grocery offers across supermarkets
- ranks stores by basket price
- considers distance to stores
- recommends the best shopping option

---

## MVP Scope
The MVP focuses on a small but complete grocery comparison workflow:
* One city in Germany: Rosenheim
* A small set of supermarkets
* A limited product catalog of common grocery items
* Simple shopping-list input
* Product matching for different user wordings, such as “spaghetti” and “pasta”
* Store comparison based on available offers
* Basket coverage check to show which items each store can provide
* Distance-based comparison using the user’s location
* Separate results for the cheapest store and the nearest store
* Clear display of missing items, basket price, and distance

---

## Planned Tech Stack
- Python
- FastAPI
- pandas
- numpy
- pytorch/tensorflow
- Streamlit
- sentence-transformer
- geopy
- Requests
- pytest
- scikit-learn

---

## FastAPI Backend

The project now includes a FastAPI backend to separate the frontend UI from the core grocery recommendation logic.

The Streamlit app acts as the frontend, while FastAPI exposes backend endpoints for:

- retrieving available stores
- calculating nearby stores based on user location
- running the full grocery comparison pipeline
- returning matched products, store comparison, and recommendations as JSON

Main API endpoints:

```text
GET  /
GET  /stores
POST /stores/nearby
POST /stores/nearest
POST /compare
```

---

## Project structure
```text
Grocery-deal-finder/
│
├── api/
│   └── main.py                  # FastAPI backend endpoints
│
├── app/
│   └── streamlit_app.py          # Streamlit frontend
│
├── data/
│   ├── products.csv              # Normalized product catalog
│   ├── product_aliases.csv       # Product aliases and synonym rules
│   ├── stores.csv                # Store information and coordinates
│   ├── offers.csv                # Sample supermarket offers
│   └── matcher_eval.csv          # Evaluation data for product matching
│
├── src/
│   ├── pipeline.py               # Main grocery comparison pipeline
│   ├── matcher.py                # Hybrid NLP product matcher
│   ├── matching_rules.py         # Alias and matching-rule loader
│   ├── compare.py                # Basket comparison logic
│   ├── recommend.py              # Cheapest / nearest recommendation logic
│   ├── distance.py               # Distance calculation logic
│   ├── load_data.py              # CSV data loading helpers
│   ├── evaluate_matcher.py       # Matcher evaluation script
│   └── project_rag.py            # Project Q&A retrieval assistant
│
├── tests/
│   ├── test_compare.py           # Tests for comparison logic
│   ├── test_matcher.py           # Tests for product matcher
│   └── test_pipeline.py          # Tests for main pipeline
│
├── README.md                     # Project documentation
├── roadmap.md                    # Development roadmap
├── weekly_checklist.md           # Development checklist
├── project_faq.md                # Source file for Project Q&A Assistant
├── requirements.txt              # Python dependencies
└── pytest.ini                    # Pytest configuration
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/CorbyVo/Grocery-deal-finder.git
cd Grocery-deal-finder
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn api.main:app --reload
```

After starting the backend, open the FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the Streamlit frontend

Open a second terminal and run:

```bash
streamlit run app/streamlit_app.py
```

---

## Project Status
This project is currently a working prototype. Current features:
- shopping-list input through Streamlit
- hybrid NLP product matching using semantic similarity and alias rules
- product alias data stored separately in CSV
- store comparison based on basket price and distance
- separate cheapest-store and nearest-store recommendations
- FastAPI backend for API-based comparison
- Streamlit frontend connected to the FastAPI backend
- Project Q&A Assistant using retrieval over project documents
- matcher evaluation script with a custom evaluation dataset

---

## Example Workflow
1. The user enters a shopping list in the Streamlit frontend.
2. The frontend sends the shopping list and user location to the FastAPI backend.
3. The FastAPI backend runs the grocery comparison pipeline.
4. The NLP matcher maps each raw user input to a normalized product name.
5. The app compares available offers across stores.
6. The app checks whether each store can cover the requested basket.
7. The app calculates the distance between the user and each store.
8. The app returns the cheapest store, nearest store, basket price, distance, and missing-item information.
9. The Streamlit frontend displays the matched products, store comparison, and final recommendation.

---

## Known Limitation
- Store and offer data is currently sample/manual data, not live supermarket data.
- The app currently focuses on a limited set of stores and grocery products.
- Quantity-aware basket comparison is not fully implemented yet.
- Matcher evaluation is based on a custom test set and should be expanded.
- The Project Q&A Assistant is retrieval-based and does not yet generate full LLM answers.
- Live supermarket API or flyer scraping is not implemented yet.
- OCR-based shopping-list input is planned but not implemented yet.

---

## Next Steps
Planned improvements include:
* Expand real store and offer data for Rosenheim
* Add browser-based user location input
* Improve quantity-aware basket comparison
* Add OCR input for shopping-list photos
* Improve API error handling and tests

For a more detailed development plan, see `roadmap.md`.

---

## Roadmap
See `roadmap.md`

---

## Weekly Progress
See `weekly_checklist.md`

---

## Screenshots
### Homepage
![Homepage](assets/screenshots/Homepage_2.png)  

### Grocery Comparison
![Grocery Comparison](assets/screenshots/comparison_1.png) 

### Project Q&A Assistant
![Project Q&A Assistant](assets/screenshots/project_qa.png)
