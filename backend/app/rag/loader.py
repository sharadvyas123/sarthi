import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from app.config import GITA_DATA_PATH

def load_gita_documents()-> List[Document]:
    """
    Docstring for load_gita_document
    
    :return: Description
    :rtype: List[Document]

    This function will Load Gita dataset and returns Langchain Document list  
    Without Chunking ! 
    """

    with open(GITA_DATA_PATH , "r" , encoding="utf-8-sig") as f:
        data = json.load(f)
    
    documents : List[Document] =[]

    for verse in data :
        base_meta = {
            "chapter" : verse["chapter"],
            "verse" : verse["verse"],
            "verse_id" : verse["verse_id"]
        }
        documents.append(
            Document(
                page_content=verse["sanskrit"],
                metadata= { **base_meta , "type" : "sanskrit"}
            )
        )

        if verse.get("word_meanings"):
            documents.append(
                Document(
                    page_content=verse["word_meanings"],
                    metadata= { **base_meta , "type" : "word_meanings"}
                )
            )
        
        for lang , translation in verse.get("translations" , {}).items():
            for t in translation:
                documents.append(
                    Document(
                        page_content=t['text'],
                        metadata = {
                            **base_meta ,
                            "type": "translation",
                            "language": lang,
                            "author": t["author"]
                        }
                    )
                )

        for lang, commentaries in verse.get("commentary", {}).items():
            for c in commentaries:
                documents.append(
                    Document(
                        page_content=c["text"],
                        metadata={
                            **base_meta,
                            "type": "commentary",
                            "language": lang,
                            "author": c["author"],
                        },
                    )
                )
        
    return documents