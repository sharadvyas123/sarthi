from app.rag.loader import load_gita_documents
from app.rag.splitter import split_documents
from app.rag.vectorstore import build_vectorstore

docs = load_gita_documents()
print("Loaded docs :" ,len(docs))

split_docs = split_documents(documents=docs)
print("Split Docs : ", len(split_docs))

vector_db = build_vectorstore(split_docs)
print("Vectorstore built successfully")