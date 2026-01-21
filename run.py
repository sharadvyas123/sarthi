from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="mistral",
    base_url="http://127.0.0.1:11434",
    temperature=0
)

response = llm.invoke("Explain RAG in one line")
print(response.content)