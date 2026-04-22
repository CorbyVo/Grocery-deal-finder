from sentence_transformers import SentenceTransformer, util
from src.load_data import load_products

class ProductMatcher:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.products_df = load_products()
        self.product_names = self.products_df["normalized_name"].dropna().tolist()
        self.product_embeddings = self.model.encode(self.product_names, convert_to_tensor=True)

    def match_product(self, user_input, threshold=0.50):
        user_embedding = self.model.encode(user_input, convert_to_tensor=True)

        # compare (measure how similar) between each user_embedding against many product_embeddings,
        # the resul is a 2D similarity matrix, take the first row (to get 1D list-like tensor of score.
        similarity_scores = util.cos_sim(user_embedding, self.product_embeddings)[0]

        # return the index of the max score in the list,
        # then convert a tensor scalar into a normal Python value
        best_index = similarity_scores.argmax().item()
        best_score = similarity_scores[best_index].item()
        best_match = self.product_names[best_index]

        if best_score < threshold:
            return None, best_score
        return best_match, best_score

if __name__ == "__main__":
    matcher = ProductMatcher()

    test_inputs = [
        "whole milk",
        "spaghetti",
        "10 eggs",
        "green apple",
        "salmon"
    ]

    for item in test_inputs:
        match, score = matcher.match_product(item)
        print(f"Input: {item}")
        print(f"Matched product: {match}")
        print(f"Similarity score: {score:.4f}")
        print("-" * 40)
