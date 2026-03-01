from app.rag.retriever import get_retriever , get_shloka

def main():
    # retriever = get_retriever(
    #     k=5,
    #     filters={
    #         "type": "commentary",
    #         "language": "hindi"
    #     }
    # )

    # query = "कर्म योग क्या है?"
    # docs = retriever.invoke(query)

    # print("\nQuery:", query)
    # print("Retrieved docs:", len(docs))
    # print("=" * 80)

    # for i, doc in enumerate(docs, start=1):
    #     print(f"\n--- Document {i} ---")
    #     print("Metadata:", doc.metadata)
    #     print("Content preview:")
    #     print(doc.page_content[:400])
    #     print("-" * 80)
    
    shloka = get_shloka(chapter=13,verse=1)
    for i , doc in enumerate(shloka,start=1):
        print(f"\n--- Document {i} ---")
        print("Metadata:", doc.metadata)
        print("Content preview:")
        print(doc.page_content[:400])
        print("-" * 80)
    
if __name__ == "__main__":
    main()
