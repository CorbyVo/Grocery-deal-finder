from sentence_transformers import SentenceTransformer, util
from src.meal_assistant.recipe_text import recipe_to_text


class RecipeRetriever:
    def __init__(self, recipes):
        self.recipes = recipes
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.recipe_texts = [recipe_to_text(recipe) for recipe in self.recipes]
        self.recipe_embeddings = self.model.encode(self.recipe_texts, convert_to_tensor=True)

    def similarity_scores(self, query):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.recipe_embeddings)
        return scores[0]

    def retrieve(self, query, top_k=1):
        scores = self.similarity_scores(query)
        k = min(top_k, len(self.recipes))
        top_scores, top_indices = scores.topk(k)

        results = []
        for score, index in zip(top_scores, top_indices):
            results.append({
                "recipe": self.recipes[index.item()],
                "score": score.item()
            })

        return results

if __name__ == "__main__":
    from src.meal_assistant.recipe_loader import load_recipes

    recipes = load_recipes()
    retriever = RecipeRetriever(recipes)

    results = retriever.retrieve("I want a breakfast with yogurt and fruit",top_k=2)
    for result in results:
        print(result["recipe"]["title"], result["score"])