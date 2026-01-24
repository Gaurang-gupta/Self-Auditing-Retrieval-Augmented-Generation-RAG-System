from fastapi import FastAPI, Query
from schemas import RAGResponseSchema
from rag import run_audited_rag
import json
import time
import uuid

def log_event(event: dict):
    print(json.dumps(event, ensure_ascii=False))

app = FastAPI(
    title="Audited RAG System",
    description="RAG pipeline with query and retrieval auditing",
    version="1.0.0"
)

@app.get("/query", response_model=RAGResponseSchema)
def query_rag(
    q: str = Query(..., description="User query"),
    attempt: int = Query(1, ge=1, le=5)
):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    result = run_audited_rag(query=q, attempt=attempt)

    total_latency = round(time.time() - start_time, 3)

    log_event({
        "event": "rag_request_completed",
        "request_id": request_id,
        "query": q,
        "status": result.get("status"),
        "confidence": result.get("confidence"),
        "total_latency_sec": total_latency
    })

    result["request_id"] = request_id
    result["latency_sec"] = total_latency

    return result

