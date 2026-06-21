from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_project_documents():
    file_paths = [
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "roadmap.md",
        PROJECT_ROOT / "weekly_checklist.md",
        PROJECT_ROOT / "project_faq.md",
        PROJECT_ROOT / "src" / "matcher.py",
        PROJECT_ROOT / "src" / "pipeline.py",
        PROJECT_ROOT / "src" / "compare.py",
        PROJECT_ROOT / "src" / "recommend.py",
        PROJECT_ROOT / "tests" / "test_compare.py",
        PROJECT_ROOT / "tests" / "test_matcher.py",
    ]

    documents = []

    for path in file_paths:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            documents.append(
                {
                    "source": path.name,
                    "text": text
                }
            )
    return documents

def chunk_text(text, min_chunk_length=40):
    raw_chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    merged_chunks = []

    i = 0
    while i < len(raw_chunks):
        current_chunk = raw_chunks[i]

        # remove markdown heading markers for checking
        cleaned_current = re.sub(r"^#+\s*", "", current_chunk).strip()

        # if current chunk is too short, or looks like only a heading / title,
        # merge it with the next chunk when possible
        if (
            len(cleaned_current) < min_chunk_length
            and i + 1 < len(raw_chunks)
        ):
            next_chunk = raw_chunks[i + 1].strip()
            merged_chunk = current_chunk + " " + next_chunk
            merged_chunks.append(merged_chunk)
            i += 2
        else:
            merged_chunks.append(current_chunk)
            i += 1

    # optional second pass: remove extremely short useless chunks
    final_chunks = []
    for chunk in merged_chunks:
        cleaned_chunk = re.sub(r"\s+", " ", chunk).strip()

        # skip chunks that are basically only numbers or tiny fragments
        if re.fullmatch(r"[\d.\- ]+", cleaned_chunk):
            continue

        if len(cleaned_chunk) >= 15:
            final_chunks.append(cleaned_chunk)

    return final_chunks


def build_project_chunks():
    documents = load_project_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
            all_chunks.append(
                {
                    "source": doc["source"],
                    "chunk": chunk
                }
            )

    return all_chunks


class ProjectRetriever:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.project_chunks = build_project_chunks()
        self.chunk_texts = [row["chunk"] for row in self.project_chunks]
        self.chunk_embeddings = self.model.encode(
            self.chunk_texts,
            convert_to_tensor=True
        )

    def retrieve(self, question, top_k=5, min_score=0.20):
        question_embedding = self.model.encode(question, convert_to_tensor=True)
        similarity_scores = util.cos_sim(question_embedding, self.chunk_embeddings)[0]

        query_words = set(re.findall(r"\w+", question.lower()))

        scored_results = []

        for idx, base_score in enumerate(similarity_scores):
            chunk_text = self.project_chunks[idx]["chunk"]
            chunk_words = set(re.findall(r"\w+", chunk_text.lower()))

            keyword_overlap = len(query_words & chunk_words)
            boosted_score = base_score.item() + 0.03 * keyword_overlap

            if boosted_score >= min_score:
                scored_results.append(
                    {
                        "index": idx,
                        "score": round(boosted_score, 4)
                    }
                )

        scored_results = sorted(scored_results, key=lambda x: x["score"], reverse=True)[:top_k]

        top_results = []
        for row in scored_results:
            idx = row["index"]
            top_results.append(
                {
                    "source": self.project_chunks[idx]["source"],
                    "chunk": self.project_chunks[idx]["chunk"],
                    "score": row["score"]
                }
            )

        return top_results