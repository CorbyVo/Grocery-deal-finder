# Student Grocery Deal Finder - Weekly Checklist

Use this file to track your work every week.

## Status legend
- [ ] not started
- [x] done
- [-] partially done / in progress

---

## Week 1 - Project setup
**Goal:** create a clean project base.

### Tasks
- [ ] Create GitHub repository
- [ ] Choose final project name
- [ ] Create repo folder structure
- [ ] Add README.md with problem and goal
- [ ] Add requirements.txt
- [ ] Add .gitignore
- [ ] Add roadmap file

### Deliverables
- [ ] Public GitHub repo created
- [ ] Basic project structure visible

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 2 - Data design
**Goal:** define how project data will be stored.

### Tasks
- [ ] Choose 1 city
- [ ] Choose 2 supermarkets
- [ ] Define 20-30 grocery products
- [ ] Create stores.csv
- [ ] Create products.csv
- [ ] Create offers.csv
- [ ] Add first manual sample offers

### Deliverables
- [ ] Three CSV files created
- [ ] Sample data can be loaded successfully

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 3 - Data loading and inspection
**Goal:** load and inspect data in Python.

### Tasks
- [ ] Write load_data.py
- [ ] Load all CSV files using pandas
- [ ] Print and inspect tables
- [ ] Check for missing values or formatting issues
- [ ] Standardize product names to lowercase / consistent format

### Deliverables
- [ ] Data loads without error
- [ ] Data cleaned enough for first logic tests

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 4 - Basket comparison logic
**Goal:** compare shopping basket totals across stores.

### Tasks
- [ ] Write compare.py
- [ ] Accept a small shopping list as input
- [ ] Match shopping list items to normalized product names
- [ ] Sum basket price by store
- [ ] Show cheapest store result

### Deliverables
- [ ] Script outputs basket total per store
- [ ] Cheapest store identified correctly

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 5 - Product matching
**Goal:** handle messy user input better.

### Tasks
- [ ] Add rapidfuzz dependency
- [ ] Write matcher.py
- [ ] Match terms like "vollmilch" and "milk 1l" to "milk"
- [ ] Test matching with at least 10 sample user inputs
- [ ] Create a small synonym list for common items

### Deliverables
- [ ] Product matching works for basic variations
- [ ] Matching logic documented

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 6 - Location and distance logic
**Goal:** recommend stores using distance, not only price.

### Tasks
- [ ] Add user location input format
- [ ] Store latitude and longitude in stores.csv
- [ ] Use geopy or simple coordinates for distance calculation
- [ ] Compute store distance from user
- [ ] Show nearest store result

### Deliverables
- [ ] Distance is calculated for all stores
- [ ] App can identify nearest store

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 7 - Recommendation engine
**Goal:** combine price and distance into a useful recommendation.

### Tasks
- [ ] Write recommend.py
- [ ] Return cheapest store
- [ ] Return nearest store
- [ ] Return best overall store
- [ ] Add simple explanation rules

### Deliverables
- [ ] Recommendation output is understandable
- [ ] One test case with clear explanation created

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 8 - Streamlit interface
**Goal:** build a simple demo interface.

### Tasks
- [ ] Create streamlit_app.py
- [ ] Add shopping list text input
- [ ] Add location input
- [ ] Display matched items
- [ ] Display price comparison table
- [ ] Display recommendation summary

### Deliverables
- [ ] Streamlit app runs locally
- [ ] End-to-end demo works with sample data

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 9 - Testing and debugging
**Goal:** make the project more reliable.

### Tasks
- [ ] Add tests folder
- [ ] Write test for matcher
- [ ] Write test for basket comparison
- [ ] Fix bugs found during testing
- [ ] Check edge cases such as missing product offers

### Deliverables
- [ ] At least 2-4 basic tests added
- [ ] Main demo path works without crashes

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 10 - Documentation polish
**Goal:** make the repo clear for recruiters.

### Tasks
- [ ] Improve README structure
- [ ] Add architecture overview
- [ ] Add sample input and output examples
- [ ] Add screenshots of app
- [ ] Add future work section

### Deliverables
- [ ] README is professional and readable
- [ ] Repo can be understood without asking you questions

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 11 - Portfolio improvement
**Goal:** make the project look stronger on GitHub and CV.

### Tasks
- [ ] Clean file names and code organization
- [ ] Improve comments in important files
- [ ] Review commit history quality
- [ ] Add one notebook or diagram if useful
- [ ] Draft CV bullet points from project

### Deliverables
- [ ] Repo looks tidy and intentional
- [ ] Project summary ready for CV or interview

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Week 12 - Final review and next-step planning
**Goal:** finish MVP and define next version.

### Tasks
- [ ] Review all features against MVP scope
- [ ] Fix final bugs
- [ ] Mark completed roadmap items
- [ ] Write lessons learned section
- [ ] Plan version 2 improvements

### Deliverables
- [ ] MVP completed
- [ ] Next version priorities written down

### Notes
- Problems faced:
- Decisions made:
- Next focus:

---

## Final MVP checklist
- [ ] GitHub repo created and organized
- [ ] Sample grocery data prepared
- [ ] Basket comparison logic works
- [ ] Product matching works for simple inputs
- [ ] Distance calculation works
- [ ] Recommendation engine works
- [ ] Streamlit demo runs locally
- [ ] README is polished
- [ ] Screenshots added
- [ ] Project is ready to show on CV
