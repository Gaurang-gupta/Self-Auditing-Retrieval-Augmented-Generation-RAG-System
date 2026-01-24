import re
from typing import Dict

# Query Auditor
# Intentionally small and deterministic
STOPWORDS = {
    "how", "does", "do", "is", "are", "was", "were",
    "this", "that", "it", "they", "them",
    "work", "works", "working", "explain", "explanation",
    "system", "thing", "stuff", "process",
    "what", "why", "when", "where", "who", "an", "the", "if"
}

def count_noun_like_tokens(text: str) -> int:
    """
    Counts content-bearing tokens.
    This is a heuristic, not linguistic analysis.
    """
    tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_-]{2,}\b", text.lower())

    meaningful_tokens = [
        t for t in tokens
        if t not in STOPWORDS
    ]

    return len(meaningful_tokens)

def compute_query_specificity(query: str) -> float:
    """
    Returns specificity score in range [0, 1].
    """
    noun_like_count = count_noun_like_tokens(query)

    # 4 meaningful tokens is "specific enough" for MVP
    raw_score = noun_like_count / 4.0
    return min(1.0, raw_score)

def audit_query(
    query: str,
    attempt: int = 1,
    max_attempts: int = 2
) -> Dict:
    """
    Pre-retrieval query auditor.
    Decides whether to proceed or request clarification.
    """

    specificity = compute_query_specificity(query)

    if specificity < 0.3 and attempt <= max_attempts:
        decision = "clarify"
        reason = "Query is underspecified"
        query_type = "underspecified"
    elif specificity < 0.3:
        decision = "proceed"
        reason = "Low specificity override after retries"
        query_type = "underspecified"
    else:
        decision = "proceed"
        reason = None
        query_type = "concrete"

    return {
        "decision": decision,
        "query_type": query_type,
        "metrics": {
            "specificity_score": round(specificity, 3)
        },
        "reason": reason
    }

# Query auditor testing
# qa1 = audit_query("How does this work?")
# qa2 = audit_query("How is logging configured in the auth service?")
# qa3 = audit_query("Explain this", attempt=3)
#
# print(qa1)
# print(qa2)
# print(qa3)

print("\n\n\n")
# Retrieval Auditor
MIN_TOP_SCORE = 0.6
MIN_MEAN_SCORE = 0.45
MAX_SCORE_SPREAD = 0.25

def compute_retrieval_metrics(retrieved_docs):
    if not retrieved_docs:
        return {
            "top_score": 0.0,
            "mean_score": 0.0,
            "score_spread": 1.0
        }

    scores = [doc["score"] for doc in retrieved_docs]

    top_score = max(scores)
    mean_score = sum(scores) / len(scores)
    score_spread = max(scores) - min(scores)

    return {
        "top_score": round(top_score, 3),
        "mean_score": round(mean_score, 3),
        "score_spread": round(score_spread, 3)
    }

def audit_retrieval(retrieved_docs):
    """
    Post-retrieval auditor.
    Decides whether generation should happen.
    """

    metrics = compute_retrieval_metrics(retrieved_docs)

    if metrics["top_score"] < MIN_TOP_SCORE:
        decision = "abstain"
        reason = "Top similarity score too low"
    elif metrics["mean_score"] < MIN_MEAN_SCORE:
        decision = "abstain"
        reason = "Mean similarity score too low"
    elif metrics["score_spread"] > MAX_SCORE_SPREAD:
        decision = "abstain"
        reason = "High score variance across retrieved documents"
    else:
        decision = "answer"
        reason = None

    # Confidence is intentionally conservative
    confidence = round(
        min(
            metrics["top_score"],
            1.0 - metrics["score_spread"]
        ),
        3
    )

    return {
        "decision": decision,
        "confidence": confidence,
        "metrics": metrics,
        "reason": reason
    }

# Retrieval auditor testing
# ra1 = [
#     {"content": "A", "score": 0.82},
#     {"content": "B", "score": 0.74},
#     {"content": "C", "score": 0.70},
# ]
# print(audit_retrieval(ra1))
#
# ra2 = [
#     {"content": "A", "score": 0.41},
#     {"content": "B", "score": 0.38}
# ]
# print(audit_retrieval(ra2))
#
# ra3 = [
#     {"content": "A", "score": 0.91},
#     {"content": "B", "score": 0.32}
# ]
# print(audit_retrieval(ra3))
