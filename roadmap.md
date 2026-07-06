# Grocery Deal Finder — Roadmap

## 1. Project Summary

Grocery Deal Finder is an AI-assisted grocery comparison prototype for students in Germany.

The app allows users to enter a shopping list, matches the input to known grocery products, compares available store offers, and shows both the cheapest store and the nearest store.

The project is designed as a practical portfolio project that demonstrates Python, data processing, NLP matching, API development, and frontend-backend separation.

---

## 2. Problem

Students and budget-conscious shoppers often need to check several supermarket flyers, apps, or websites to find the best grocery deals.

This is time-consuming because product names are not always written the same way, prices are spread across different sources, and users also need to consider the distance to the store.

---

## 3. Goal

The goal is to build a working prototype that can:

* accept a user shopping list
* normalize product names using matching logic
* compare grocery offers across stores
* calculate store distance from the user
* show the cheapest store
* show the nearest store
* explain the recommendation clearly
* expose the core logic through a FastAPI backend

---

## 4. Target Users

* students in Germany
* budget-conscious shoppers
* people who want to compare supermarket offers faster
* users who want a simple grocery recommendation based on price and distance

---

## 5. Current Features

The current version includes:

* Streamlit frontend
* FastAPI backend
* shopping-list input
* hybrid product matching
* alias-based matching rules
* semantic similarity matching using Sentence Transformers
* store comparison based on basket price
* distance calculation based on user location
* separate cheapest-store and nearest-store recommendations
* optional AI matching details in the UI
* Project Q&A Assistant using retrieval over project documents
* matcher evaluation script with a custom evaluation dataset
* basic tests for matcher, comparison, and pipeline logic

---

## 6. Current Architecture

```text
User
 |
 v
Streamlit Frontend
 |
 | sends shopping list + location
 v
FastAPI Backend
 |
 v
Pipeline Logic
 |
 |-- Product Matcher
 |-- Store Comparison
 |-- Distance Calculation
 |-- Recommendation Logic
 |
 v
JSON Result
 |
 v
Streamlit Display
```

The Streamlit app is used as the frontend.

The FastAPI backend exposes the project logic through API endpoints.

The core recommendation logic remains reusable inside the `src/` folder.

---

## 7. Main API Endpoints

```text
GET  /
GET  /stores
POST /stores/nearby
POST /stores/nearest
POST /compare
```

The main endpoint is:

```text
POST /compare
```

This endpoint receives:

* shopping list
* user latitude
* user longitude
* matching threshold

It returns:

* matched products
* unmatched user inputs
* store comparison
* cheapest-store and nearest-store recommendation message

---

## 8. Development Phases

### Phase 1 — Proof of Concept

Completed:

* created project repository
* created basic folder structure
* created sample CSV data
* built basket comparison logic
* built initial recommendation logic

### Phase 2 — Streamlit Prototype

Completed:

* built Streamlit interface
* added shopping-list input
* displayed matched products
* displayed store comparison
* displayed recommendation message

### Phase 3 — NLP Product Matching

Completed:

* added semantic product matching
* added alias and synonym matching
* moved matching rules into CSV
* added confidence and method labels
* added matcher evaluation script
* created custom matcher evaluation dataset

### Phase 4 — Recommendation Improvements

Completed:

* added distance calculation
* separated cheapest store and nearest store
* avoided artificial combined scoring
* improved handling of unmatched products
* improved display formatting in Streamlit

### Phase 5 — Project Q&A Assistant

Completed:

* added retrieval-based project assistant
* used README, roadmap, FAQ, checklist, and source files as retrieval sources
* added chat-style interface
* added retrieved source display

### Phase 6 — FastAPI Backend

Completed:

* created FastAPI backend
* added store-location endpoints
* added nearby-store endpoint
* added nearest-store endpoint
* added `/compare` endpoint
* connected Streamlit frontend to FastAPI backend

---

## 9. Main Engineering Challenge

The biggest challenge is not the recommendation formula.

The hardest part is obtaining and maintaining reliable grocery offer data, because supermarket prices, product names, units, and discounts change frequently.

For this reason, the current version uses manually curated sample data.

---

## 10. Current Limitations

* Store and offer data is manually created sample data.
* The app does not yet use live supermarket data.
* The number of products and stores is still limited.
* Quantity-aware basket comparison is not fully implemented yet.
* OCR-based shopping-list input is not implemented yet.
* Product-package image recognition is not implemented.
* The Project Q&A Assistant is retrieval-based, not a full LLM answer generator.
* Real walking or public transport route calculation is not implemented yet.

---

## 11. Next Steps

### Short-Term Improvements

* update README with FastAPI setup instructions
* add screenshots of the Streamlit app and FastAPI docs
* improve API error handling
* improve empty-result handling in Streamlit
* expand Rosenheim store data
* expand grocery offer data

### Medium-Term Improvements

* add quantity handling
* improve matcher evaluation dataset
* add more realistic grocery input examples
* add browser-based location input
* add SQLite database instead of CSV-only storage
* add better API response models

### Long-Term Ideas

* semi-automated flyer or offer extraction
* OCR input for shopping-list photos
* basket optimization across multiple stores
* historical price tracking
* support more cities
* support more supermarket chains
* route-aware recommendation using walking or public transport distance

---

## 12. What This Project Demonstrates

This project demonstrates:

* practical Python development
* clean project structure
* data processing with pandas
* NLP-based product matching
* API development with FastAPI
* frontend-backend separation
* Streamlit app development
* testing and evaluation mindset
* product thinking
* clear documentation
