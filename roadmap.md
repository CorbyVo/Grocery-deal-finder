# Student Grocery Deal Finder - Project Roadmap

## 1. Project summary
A beginner-friendly AI-assisted prototype that helps students in Germany compare supermarket offers and find the best nearby store based on basket price and distance.

## 2. Problem
Students often need to check multiple supermarket flyers and apps to find the best grocery discounts. This is time-consuming and makes it harder to save money.

## 3. Goal
Build a working prototype that:
- accepts a shopping list from the user
- compares selected supermarket offers
- considers store distance from the user
- recommends the best store
- explains the recommendation clearly

## 4. Target users
- students in Germany
- budget-conscious shoppers
- people who do not want to manually compare flyers

## 5. MVP scope
To keep the project realistic and finishable, the first version will include:
- 1 city in Germany
- 2 supermarkets only
- 20-30 common grocery products
- manually curated weekly offer data
- shopping-list comparison
- distance-aware recommendation
- simple AI/NLP product matching

## 6. Key features by phase

### Phase 1 - Proof of concept
- Create project repo and folder structure
- Create sample CSV files for stores, products, and offers
- Build basket price comparison logic

### Phase 2 - Useful prototype
- Add distance calculation
- Add recommendation logic
- Build a simple Streamlit interface

### Phase 3 - AI enhancement
- Semantic product matching using a pretrained Sentence Transformer (SBERT-style) model
- Normalize user input to known products
- Add natural-language recommendation explanation

### Phase 4 - Portfolio polish
- Improve README and documentation
- Add screenshots and demo examples
- Add tests for matching and comparison logic

### Phase 5 - Future expansion
- Add more supermarkets
- Semi-automate data collection
- Introduce database storage
- Expose functionality through an API

## 7. Technical architecture

### Frontend
- Streamlit

### Core logic
- Python
- pandas
- sentence-transformer
- geopy

### Storage
- CSV initially
- SQLite later

### Possible later additions
- FastAPI
- embeddings or LLM-based matching
- automated ingestion pipeline

## 8. Main engineering challenge
The hardest part of the project is not the recommendation logic. It is obtaining and maintaining reliable supermarket offer data.

## 9. Data strategy

### Stage 1
Manual sample data entered into CSV files.

### Stage 2
Semi-automated extraction from public flyer/web sources.

### Stage 3
Normalization pipeline for product names, units, and categories.

### Stage 4
Potential future combination with crowdsourced or partner data.

## 10. Success criteria for MVP
The MVP is successful if a user can:
- enter a small shopping list
- see matched products
- compare basket prices across two stores
- see which store is cheapest
- see which store is nearer
- receive a clear recommendation

## 11. Repository structure
```text
student-grocery-deal-finder/
|- data/
|  |- stores.csv
|  |- products.csv
|  `- offers.csv
|- src/
|  |- load_data.py
|  |- matcher.py
|  |- compare.py
|  |- recommend.py
|  `- utils.py
|- app/
|  `- streamlit_app.py
|- tests/
|- notebooks/
|- README.md
|- requirements.txt
`- roadmap.md
```

## 12. What recruiters should see
This project should demonstrate:
- problem-solving ability
- clean project structure
- practical use of Python and data processing
- understanding of AI as a focused tool rather than a buzzword
- product thinking and clear documentation

## 13. Future work ideas
- add public transport or walking route suggestions
- improve product matching with embeddings
- add basket optimization across multiple stores
- track historical offer trends
- support more cities and more chains

## 14. One-sentence CV version
Built an AI-assisted grocery price comparison prototype for students in Germany that ranks nearby supermarkets based on basket price and distance using Python, data processing, and product-matching logic.
