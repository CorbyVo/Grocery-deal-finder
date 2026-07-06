# Student Grocery Deal Finder - Weekly Checklist

Use this file to track your work every week.

## Status legend
- [ ] not started
- [x] done
- [-] partially done / in progress

---

## Week 1 - Project setup and Data design
**Goal:** create a clean project base and define how project data will be stored

### Tasks
- [x] Create GitHub repository
- [x] Choose final project name
- [x] Create repo folder structure
- [x] Add README.md with problem and goal
- [x] Add requirements.txt
- [x] Add .gitignore
- [x] Add roadmap file

### Deliverables
- [x] Public GitHub repo created
- [x] Basic project structure visible

### Tasks
- [x] Choose 1 city
- [x] Choose 2 supermarkets
- [ ] Define 20-30 grocery products
- [x] Create stores.csv
- [x] Create products.csv
- [x] Create offers.csv
- [x] Add first manual sample offers

### Deliverables
- [x] Three CSV files created
- [x] Sample data can be loaded successfully

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 2 - Data loading and inspection
**Goal:** load and inspect data in Python.

### Tasks
- [x] Write load_data.py
- [x] Load all CSV files using pandas
- [x] Print and inspect tables
- [ ] Check for missing values or formatting issues
- [ ] Standardize product names to lowercase / consistent format

### Deliverables
- [x] Data loads without error
- [x] Data cleaned enough for first logic tests

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 3 - Basket comparison logic
**Goal:** compare shopping basket totals across stores.

### Tasks
- [x] Write compare.py
- [x] Accept a small shopping list as input
- [x] Match shopping list items to normalized product names
- [x] Sum basket price by store
- [x] Show cheapest store result

### Deliverables
- [x] Script outputs basket total per store
- [x] Cheapest store identified correctly

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 4 - Product matching
**Goal:** handle messy user input better.

### Tasks
- [x] Write matcher.py
- [x] Match terms like "vollmilch" and "milk 1l" to "milk"
- [ ] Test matching with at least 10 sample user inputs
- [ ] Create a small synonym list for common items

### Deliverables
- [x] Product matching works for basic variations
- [x] Matching logic documented

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 5 - Location and distance logic
**Goal:** recommend stores using distance, not only price.

### Tasks
- [x] Add user location input format
- [x] Store latitude and longitude in stores.csv
- [x] Use geopy or simple coordinates for distance calculation
- [x] Compute store distance from user
- [x] Show nearest store result

### Deliverables
- [x] Distance is calculated for all stores
- [x] App can identify nearest store

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 6 - Recommendation engine

Goal: provide useful store recommendations based on price and distance.

### Tasks

- [x] Write `recommend.py`
- [x] Return cheapest store
- [x] Return nearest store
- [x] Add simple explanation rules
- [x] Explain tradeoff when cheapest and nearest stores are different

### Deliverables

- [x] Cheapest store is shown correctly
- [x] Nearest store is shown correctly
- [x] Recommendation message is understandable
- [x] User can compare price and distance separately

### Notes

Problems faced: It was difficult to create one fair "best overall store" because price and distance use different scales and the final choice depends on the user's personal preference.

Decisions made: Do not force one combined score. Show cheapest store and nearest store separately, then explain the tradeoff clearly.

Next focus: Improve recommendation explanation and maybe add optional user preference later, such as "prefer cheapest" or "prefer nearest".


---

## Week 7 - Streamlit interface
**Goal:** build a simple demo interface.

### Tasks
- [x] Create streamlit_app.py
- [x] Add shopping list text input
- [x] Add location input
- [x] Display matched items
- [x] Display price comparison table
- [x] Display recommendation summary

### Deliverables
- [x] Streamlit app runs locally
- [x] End-to-end demo works with sample data

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 8 - Testing and debugging
**Goal:** make the project more reliable.

### Tasks
- [X] Add tests folder
- [X] Write test for matcher
- [X] Write test for basket comparison
- [ ] Fix bugs found during testing
- [ ] Check edge cases such as missing product offers

### Deliverables
- [X] At least 2-4 basic tests added
- [ ] Main demo path works without crashes

---

## Week 9 - Documentation polish
**Goal:** make the repo clear for recruiters.

### Tasks
- [X] Improve README structure
- [X] Add architecture overview
- [X] Add sample input and output examples
- [X] Add screenshots of app
- [X] Add future work section

### Deliverables
- [X] README is professional and readable
- [X] Repo can be understood without asking you questions

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 10 - Portfolio improvement
**Goal:** make the project look stronger on GitHub and CV.

### Tasks
- [X] Clean file names and code organization
- [X] Improve comments in important files
- [X] Review commit history quality
- [X] Add one notebook or diagram if useful
- [X] Draft CV bullet points from project

### Deliverables
- [ ] Repo looks tidy and intentional
- [ ] Project summary ready for CV or interview

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 11 - Final review and next-step planning
**Goal:** finish MVP and define next version.

### Tasks
- [X] Review all features against MVP scope
- [ ] Fix final bugs
- [X] Mark completed roadmap items
- [ ] Write lessons learned section
- [ ] Plan version 2 improvements

### Deliverables
- [X] MVP completed
- [ ] Next version priorities written down

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Final MVP checklist
- [x] GitHub repo created and organized
- [x] Sample grocery data prepared
- [x] Basket comparison logic works
- [X] Product matching works for simple inputs
- [X] Distance calculation works
- [X] Recommendation engine works
- [X] Streamlit demo runs locally
- [X] README is polished
- [X] Screenshots added
- [X] Project is ready to show on CV

## Week 12 - FastAPI Backend

Goal: separate the frontend from the backend and expose the project logic through API endpoints.

### Tasks

- [x] Create `api/main.py`
- [x] Add FastAPI app
- [x] Add `/stores` endpoint
- [x] Add `/stores/nearby` endpoint
- [x] Add `/stores/nearest` endpoint
- [x] Add `/compare` endpoint
- [x] Connect Streamlit frontend to FastAPI using `requests`
- [x] Convert pandas DataFrame results into JSON-safe response

### Deliverables

- [x] FastAPI backend runs locally
- [x] API documentation is available at `/docs`
- [x] Streamlit sends shopping list and user location to FastAPI
- [x] FastAPI runs the recommendation pipeline
- [x] Streamlit displays the API response

### Notes

- Problems faced: Streamlit originally called the Python pipeline directly, so the app did not clearly show frontend-backend separation.

- Decisions made: Keep Streamlit as the frontend and use FastAPI as the backend. The existing matcher, comparison, and recommendation logic stays reusable inside the backend.

- Next focus: Update README, requirements.txt, roadmap, and project structure to show the new FastAPI architecture.

