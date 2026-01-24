from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class TimingSchema(BaseModel):
    vectorstore_load: Optional[float] = None
    query_audit: Optional[float] = None
    retrieval: Optional[float] = None
    retrieval_audit: Optional[float] = None
    generation: Optional[float] = None

class QueryAuditSchema(BaseModel):
    decision: str
    query_type: str
    metrics: Dict[str, float]
    reason: Optional[str]


class RetrievalAuditSchema(BaseModel):
    decision: str
    confidence: float
    metrics: Dict[str, float]
    reason: Optional[str]


class RetrievedChunkSchema(BaseModel):
    content: str
    score: float
    metadata: Dict[str, Any]


class RAGResponseSchema(BaseModel):
    status: str
    answer: Optional[str] = None
    confidence: Optional[float] = None

    query_audit: Optional[QueryAuditSchema] = None
    retrieval_audit: Optional[RetrievalAuditSchema] = None
    retrieved_chunks: Optional[List[RetrievedChunkSchema]] = None

    timings: Optional[TimingSchema] = None
