from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


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
        chunk_size = 700,
        chunk_overlap=100,
        separators=["\n\n" , "\n" , "|" , "."]
    )

    for doc in documents:

        if doc.metadata.get("type") in ["sanskrit" , "translation" , "word_meaning"]:
            split_docs.append(doc)
            continue
        else :
            chunks = commentary_splitter.split_text(doc.page_content)

            for idx , chunk in enumerate(chunks):
                split_docs.append(
                    Document(
                        page_content=chunk.strip(),
                        metadata={**doc.metadata , "chunk_index" : idx}
                    )
                )
    
    return split_docs
