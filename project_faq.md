What does this project do?
This project is a grocery deal finder prototype for students in Germany. It matches user shopping-list inputs to normalized product names, compares supermarket offer data, and recommends the cheapest and nearest store.

How does product matching work?
The project uses Sentence Transformers for semantic matching. This helps map inputs like "spaghetti" to normalized product names like "pasta".

How are unmatched user inputs handled?
If a user input cannot be matched to the product catalog with enough confidence, it is stored separately as an unmatched user input and shown in the interface.

How does store comparison work?
The app compares available offers by store, checks how many original requests are covered, calculates distance to stores, and then identifies the cheapest and nearest store.

What are the current limitations?
The project currently uses sample data, covers only a small set of products and stores, and does not yet have a live supermarket data pipeline.

What are the next steps?
Next improvements include better test coverage, quantity-aware basket comparison, expanding store and product data, improving recommendation logic, and exploring automated data ingestion.