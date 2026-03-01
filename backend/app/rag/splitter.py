from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

MAX_COMMENTARY_CHARS =600

def split_documents(documents : List[Document])-> List[Document] :
    """
    Docstring for split_documents
    
    :param documents: Description
    :type documents: List[Document]
    :return: Description
    :rtype: List[Document]

    This function will split the documents which are getting from loader.py's function
    this function will split only commentary cause sanskrit and translation splitting will break the purpose ! 
    commentary is useful

    """
    split_docs : List[Document] = []

    commentary_splitter = RecursiveCharacterTextSplitter(
        chunk_size = MAX_COMMENTARY_CHARS,
        chunk_overlap=80,
        separators=["\n\n" , "\n" ,"।", "|" , "."]
    )

    for doc in documents:

        if doc.metadata.get("type") in ["sanskrit" , "translation" , "word_meaning"]:
            split_docs.append(doc)
            continue
        if doc.metadata.get("type") == "commentary" :
            text = doc.page_content.strip()

            if len(text) <= MAX_COMMENTARY_CHARS:
                split_docs.append(
                    Document(
                        page_content=text,
                        metadata = {
                            **doc.metadata,
                            "chunk_index": 0,
                            "chunk_total": 1
                        }
                    )
                )
            else :
                chunks = commentary_splitter.split_text(text=text)
                for idx , chunk in enumerate(chunks):
                    split_docs.append(
                        Document(
                            page_content=chunk.strip(),
                            metadata ={
                                **doc.metadata,
                                "chunk_index": idx,
                                "chunk_total": len(chunks)
                            }
                        )
                    )
    
    return split_docs
