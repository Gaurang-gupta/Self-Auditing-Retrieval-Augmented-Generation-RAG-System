# Self-Auditing Retrieval-Augmented Generation (RAG) System

A production-style Retrieval-Augmented Generation (RAG) system with explicit auditing layers that decide whether the system should answer at all, instead of blindly generating responses.

This project treats hallucination, irrelevance, and underspecified queries as system design failures, not prompt failures.

## Why This Project Exists

Most RAG systems fail silently:

1. They retrieve weak or inconsistent documents
2. They answer underspecified questions confidently
3. They provide no signal about why an answer should be trusted

This project addresses that by introducing deterministic auditors before and after retrieval, enforcing strict decision boundaries.

## High-Level Architecture
```
User Query
   │
   ▼
Query Auditor (pre-retrieval)
   │
   ├── clarify → stop
   └── proceed
           │
           ▼
     Vector Retrieval (FAISS)
           │
           ▼
 Retrieval Auditor (post-retrieval)
           │
   ├── abstain → stop
   └── answer
           │
           ▼
    Controlled Generation (LLM)
           │
           ▼
 Structured API Response
```

## Key Design Principles
1. Never trust the LLM by default
2. Audit before generation
3. Confidence must come from evidence, not model output
4. Every decision must be inspectable

## Core Components
### 1. Query Auditor (Pre-Retrieval)

Blocks underspecified or vague queries before retrieval.

Heuristics used:

1. Content-bearing token count
2. Stopword filtering
3. Specificity scoring

Outcomes:

1. `clarify` → system refuses to answer
2. `proceed` → retrieval allowed

This prevents wasting compute on bad questions.

### 2. Retrieval Engine

1. Document chunking with overlap
2. Sentence-transformer embeddings
3. FAISS vector index
4. Top-k similarity search

### 3. Retrieval Auditor (Post-Retrieval)

Validates whether retrieved documents are strong and consistent enough to justify generation.

Metrics evaluated:
1. Top similarity score
2. Mean similarity score
3. Score variance across retrieved chunks

Outcomes:
1. `answer` → generation allowed
2. `abstain` → system refuses to answer

This prevents hallucination from weak or conflicting context.

### 4. Controlled Generation

1. LLM is restricted to retrieved context only
2. Explicit instruction to admit missing information
3. No open-ended generation

### 5. Observability & Metrics

Each request emits:
1. Query audit decision
2. Retrieval audit decision
3. Confidence score (derived from retrieval quality)
4. Per-stage latency metrics

This makes failures measurable and debuggable.

## API Design
### Endpoint
`GET /query?q=<query>&attempt=<n>`

### Example Response (Clarification Required)
```bash
{
  "status": "clarification_required",
  "answer": null,
  "confidence": null,
  "query_audit": {
    "decision": "clarify",
    "query_type": "underspecified",
    "metrics": {
      "specificity_score": 0.0
    },
    "reason": "Query is underspecified"
  },
  "retrieval_audit": null,
  "retrieved_chunks": null,
  "timings_ms": {
    "query_audit": 2.1
  }
}
```

### Example Response (Answer Provided)
```bash
{
  "status": "answered",
  "answer": "...",
  "confidence": 0.82,
  "query_audit": { ... },
  "retrieval_audit": { ... },
  "retrieved_chunks": [ ... ],
  "timings_ms": {
    "query_audit": 1.9,
    "retrieval": 18.4,
    "generation": 112.7
  }
}
```

## Failure Modes Explicitly Handled
1. Underspecified queries
2. Low semantic similarity retrieval
3. High variance across retrieved documents
4. False confidence from LLMs
5. Silent hallucination

## Tech Stack
1. Python
2. FastAPI
3. LangChain
4. FAISS
5. HuggingFace Transformers
6. Sentence-Transformers

## Project Structure
```bash
├── main.py              # FastAPI entrypoint
├── rag.py               # RAG pipeline logic
├── auditors.py          # Query & retrieval auditors
├── schemas.py           # Typed response schemas
├── one_time_run.py      # Embedding + FAISS index creation
├── data/
│   ├── docs/            # Source documents
│   └── faiss_index/     # Vector store
```

## How This Differs from Typical RAG Demos
| Typical RAG         | This Project              | 
|:--------------------|:--------------------------|
| Always answers      | May refuse to answer      |
| Prompt-based safety | System-level safety       |
|No confidence | Evidence-based confidence |
|Debug-unfriendly	| Fully inspectable         |


## Intended Audience
1. ML Engineers
2. Applied Scientists
3. Backend / Platform Engineers
4. Anyone building real LLM systems

## Status

This project is intentionally frozen.
The goal is correctness, clarity, and system design — not feature creep.