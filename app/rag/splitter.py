from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )

    chunked_docs = []

    for doc in documents:
        # Don't split short Sanskrit verses
        if doc.metadata["type"] == "sanskrit":
            chunked_docs.append(doc)
        else:
            splits = splitter.split_documents([doc])
            chunked_docs.extend(splits)

    return chunked_docs