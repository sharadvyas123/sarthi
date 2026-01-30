from app.rag.loader import load_gita_documents
from app.rag.splitter import split_documents

docs = load_gita_documents()
split_docs = split_documents(docs)

print(len(docs), "→", len(split_docs))
print(split_docs[0])
