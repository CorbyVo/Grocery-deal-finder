from sentence_transformers import SentenceTransformer, util
from src.load_data import load_products
from src.matching_rules import load_aliases, apply_alias_rule, normalize_text, token_overlap_score


class ProductMatcher:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.products_df = load_products()
        self.product_names = self.products_df["normalized_name"].dropna().tolist()
        self.product_embeddings = self.model.encode(self.product_names,convert_to_tensor=True)
        self.alias_dict = load_aliases()

    def match_product_detailed(self, user_input, threshold=0.50, top_k=5):
        alias_match, match_method = apply_alias_rule(user_input, self.alias_dict)

        if alias_match is not None:
            return {
                "best_match": alias_match,
                "score": 1.0,
                "confidence": "high",
                "method": match_method,
                "candidates": [
                    {
                        "product": alias_match,
                        "semantic_score": 1.0,
                        "hybrid_score": 1.0
                    }
                ]
            }

        cleaned_input = normalize_text(user_input)
        user_embedding = self.model.encode(cleaned_input, convert_to_tensor=True)

        similarity_scores = util.cos_sim(user_embedding, self.product_embeddings)[0]
        top_indices = similarity_scores.argsort(descending=True)[:top_k]

        reranked_candidates = []

        for idx in top_indices:
            idx = idx.item()
            product_name = self.product_names[idx]
            semantic_score = similarity_scores[idx].item()

            exact_bonus = 0.15 if cleaned_input == normalize_text(product_name) else 0.0
            overlap_bonus = 0.10 * token_overlap_score(cleaned_input, product_name)

            hybrid_score = min(1.0, semantic_score + exact_bonus + overlap_bonus)

            reranked_candidates.append(
                {
                    "product": product_name,
                    "semantic_score": round(semantic_score, 4),
                    "hybrid_score": round(hybrid_score, 4)
                }
            )

        reranked_candidates.sort(key=lambda x: x["hybrid_score"], reverse=True)

        best_candidate = reranked_candidates[0]
        best_match = best_candidate["product"]
        best_score = best_candidate["hybrid_score"]

        if best_score < threshold:
            return {
                "best_match": None,
                "score": best_score,
                "confidence": "low",
                "method": "semantic_rejected",
                "candidates": reranked_candidates
            }

        if best_score >= 0.80:
            confidence = "high"
        elif best_score >= 0.65:
            confidence = "medium"
        else:
            confidence = "low"

        return {
            "best_match": best_match,
            "score": best_score,
            "confidence": confidence,
            "method": "semantic_hybrid",
            "candidates": reranked_candidates
        }

    def match_product(self, user_input, threshold=0.50):
        result = self.match_product_detailed(user_input, threshold=threshold)
        return result["best_match"], result["score"]


if __name__ == "__main__":
    matcher = ProductMatcher()

    test_inputs = [
        "whole milk",
        "spaghetti",
        "10 eggs",
        "green apple",
        "salmon",
        "10 eggs"
    ]

    for item in test_inputs:
        result = matcher.match_product_detailed(item, threshold=0.50)
        print(f"Input: {item}")
        print(f"Best match: {result['best_match']}")
        print(f"Score: {result['score']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Method: {result['method']}")
        print(f"Top candidates: {result['candidates'][:3]}")
        print("-" * 50)