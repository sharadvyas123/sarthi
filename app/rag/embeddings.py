from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns the embedding model used across the Sarthi RAG system.

    This function centralizes embedding configuration so that:
    - The model can be changed in one place
    - Vectorstore and retriever remain decoupled from model choice
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )