# one time run
from rag import load_documents, chunk_documents, build_vectorstore, save_vectorstore

docs = load_documents()
chunks = chunk_documents(docs)
vectorstore = build_vectorstore(chunks)
save_vectorstore(vectorstore)

print("Vector store built successfully.")