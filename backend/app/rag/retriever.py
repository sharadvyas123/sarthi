from app.rag.embeddings import get_embedding_model
from langchain_chroma import Chroma
from app.config import CHROMA_PATH


def load_vectorstore():
    embeddings = get_embedding_model()

    return Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )


def get_retriever(
    k: int = 6,
    algorithm: str = "similarity",
    route : str | None = None,
    filters: dict | None = None,
    fetch_k: int | None = None,
    lambda_mult: float | None = None
):
    vectordb = load_vectorstore()
    search_kwargs = {"k": k}

    if route :
        route_filter = {"type" : route}
        if filters:
            filters.update(route_filter)
        else:
            filters = route_filter
            
    if filters:
        if len(filters) > 1:
            search_kwargs["filter"] = {
                "$and": [{k: v} for k, v in filters.items()]
            }
        else:
            key, value = next(iter(filters.items()))
            search_kwargs["filter"] = {key: value}

    if fetch_k is not None:
        search_kwargs["fetch_k"] = fetch_k

    if lambda_mult is not None:
        search_kwargs["lambda_mult"] = lambda_mult

    return vectordb.as_retriever(
        search_type=algorithm,
        search_kwargs=search_kwargs
    )


def get_shloka(chapter: int, verse: int):
    vectorstore =load_vectorstore()
    filter={
    "$and": [
        {"chapter": chapter},
        {"verse": verse},
        {"type" : "sanskrit"}
    ]
}

    results = vectorstore.similarity_search(
        query=" ",   # dummy query (important trick)
        k=20,
        filter=filter
    )

    return results
