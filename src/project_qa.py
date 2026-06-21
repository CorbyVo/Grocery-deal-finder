def answer_project_question(question):
    question = question.lower()

    if "what does this project do" in question or "what is this project" in question:
        return (
            "This project is a prototype grocery deal finder for students in Germany. "
            "It matches shopping-list inputs to normalized product names, compares supermarket offers, "
            "and recommends the cheapest and nearest store."
        )

    if "model" in question or "nlp" in question or "matching" in question:
        return (
            "The project uses Sentence Transformers for semantic product matching. "
            "This helps map user inputs like 'spaghetti' to normalized product names like 'pasta'."
        )

    if "limitation" in question or "limitations" in question:
        return (
            "Current limitations include sample data only, a small product catalog, "
            "limited supermarket coverage, and no live supermarket data pipeline yet."
        )

    if "next step" in question or "next steps" in question:
        return (
            "The next planned improvements are better tests, quantity-aware basket comparison, "
            "more realistic store data, and a more advanced RAG-based project assistant."
        )

    if "test" in question or "testing" in question:
        return (
            "The project currently includes tests for basket comparison logic and matcher behavior, "
            "including many-to-one normalization cases."
        )

    return (
        "I can currently answer questions about the project goal, matching logic, limitations, testing, "
        "and next steps. A retrieval-based assistant will be added next."
    )