from typing import List, Tuple
from auditors import audit_query, audit_retrieval

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

import os
import pickle
import time

DATA_DIR = "data/docs"
INDEX_PATH = "data/faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# document loading
def load_documents() -> List[Document]:
    docs = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt") or filename.endswith(".md"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                text = f.read()

            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": filename}
                )
            )

    return docs

# chunking
def chunk_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(docs)

# vector store
def build_vectorstore(chunks: List[Document]) -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore

# persistence
def save_vectorstore(vectorstore: FAISS):
    vectorstore.save_local(INDEX_PATH)


def load_vectorstore() -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

# retrieve
def retrieve(
    query: str,
    vectorstore: FAISS,
    k: int = 5
):
    results = vectorstore.similarity_search_with_score(query, k=k)

    retrieved = []
    for doc, distance in results:
        similarity = 1 / (1 + distance)

        retrieved.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": round(similarity, 3)
        })

    return retrieved


# generator
def generate_answer(query: str, docs: List[Document]) -> str:
    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
        for doc in docs
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an internal engineering knowledge assistant.

Answer the question using ONLY the provided context.
If the answer is not contained in the context, say so explicitly.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    llm = HuggingFacePipeline.from_model_id(
        model_id="google/flan-t5-base",
        task="text2text-generation",
        pipeline_kwargs={"max_new_tokens": 256}
    )

    return llm(prompt.format(context=context, question=query))

# baseline RAG
def run_baseline_rag(query: str) -> dict:
    vectorstore = load_vectorstore()

    retrieved = retrieve(query, vectorstore)
    docs = [doc for doc, _ in retrieved]

    answer = generate_answer(query, docs)

    return {
        "query": query,
        "answer": answer,
        "retrieved_chunks": [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source"),
                "similarity": score
            }
            for doc, score in retrieved
        ]
    }

# Audited RAG
def run_audited_rag(
    query: str,
    attempt: int = 1
) -> dict:
    timings = {}
    t0 = time.time()
    vectorstore = load_vectorstore()
    timings["vectorstore_load"] = round(time.time() - t0, 3)

    # 1. Query audit
    t1 = time.time()
    query_audit = audit_query(query, attempt=attempt)
    timings["query_audit"] = round(time.time() - t1, 3)

    if query_audit["decision"] == "clarify":
        return {
            "status": "clarification_required",
            "query_audit": query_audit,
            "timings": timings
        }

    # 2. Retrieval
    t2 = time.time()
    retrieved = retrieve(query, vectorstore)
    timings["retrieval"] = round(time.time() - t2, 3)

    # 3. Retrieval audit
    t3 = time.time()
    retrieval_audit = audit_retrieval(retrieved)
    timings["retrieval_audit"] = round(time.time() - t3, 3)

    if retrieval_audit["decision"] == "abstain":
        return {
            "status": "abstained",
            "confidence": retrieval_audit["confidence"],
            "retrieval_audit": retrieval_audit,
            "timings": timings
        }

    # 4. Generation
    t4 = time.time()
    docs_for_generation = [
        Document(
            page_content=doc["content"],
            metadata=doc["metadata"]
        )
        for doc in retrieved
    ]

    answer = generate_answer(query, docs_for_generation)
    timings["generation"] = round(time.time() - t4, 3)

    return {
        "status": "answered",
        "answer": answer,
        "confidence": retrieval_audit["confidence"],
        "query_audit": query_audit,
        "retrieval_audit": retrieval_audit,
        "retrieved_chunks": retrieved,
        "timings": timings
    }


