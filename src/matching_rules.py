import re
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_aliases(path=None) -> dict:
    if path is None:
        path = PROJECT_ROOT / "data" / "product_aliases.csv"

    df = pd.read_csv(path)
    alias_dict = {}

    for _, row in df.iterrows():
        alias = normalize_text(str(row["alias"]))
        target = normalize_text(str(row["target"]))
        alias_dict[alias] = target

    return alias_dict


def apply_alias_rule(user_input: str, alias_dict: dict):
    normalized_input = normalize_text(user_input)

    # 1. exact full match
    if normalized_input in alias_dict:
        return alias_dict[normalized_input], "alias_exact"

    input_tokens = set(normalized_input.split())

    # 2. try longer aliases first
    sorted_aliases = sorted(alias_dict.items(), key=lambda x: len(x[0].split()), reverse=True)

    for alias, target in sorted_aliases:
        alias_tokens = set(alias.split())

        if alias_tokens.issubset(input_tokens):
            return target, "alias_contains"

    return None, None


def token_overlap_score(user_input: str, candidate_product: str) -> float:
    input_tokens = set(normalize_text(user_input).split())
    candidate_tokens = set(normalize_text(candidate_product).split())

    if not input_tokens or not candidate_tokens:
        return 0.0

    overlap = len(input_tokens & candidate_tokens)
    union = len(input_tokens | candidate_tokens)

    return overlap / union if union > 0 else 0.0