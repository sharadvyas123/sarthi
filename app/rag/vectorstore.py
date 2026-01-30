from langchain_core.vectorstores import Chroma
from app.rag.embeddings import get_embedding_model
from app.config import CHROMA_PATH
import os, shutil

def build_vectorstore(documents):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

def build_vectorstore(documents):
    embeddings = get_embedding_model()

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    vectordb.persist()
    return vectordb