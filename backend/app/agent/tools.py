import re
from typing import List , Optional , Tuple
from langchain_core.documents import Document
from app.rag.retriever import get_retriever , get_shloka


REFERENCE_PATTERNS = [

    # chapter 13 verse 2
    r'chapter\s*(\d{1,2})\D+verse\s*(\d{1,3})',

    # verse 2 chapter 13
    r'verse\s*(\d{1,3})\D+chapter\s*(\d{1,2})',

    # 13.2 or 13:2
    r'\b(\d{1,2})[.:](\d{1,3})\b',

    # BG 13.2 / Gita 13.2
    r'(?:bg|gita)\s*(\d{1,2})[.:](\d{1,3})',
]


def retrieve_gita_docs(question :str, search_type:str , filters : dict|None = None)->List[Document]:
    """
    Docstring for retrieve_gita_docs
    
    :param question: Description
    :type question: str
    :param vectorstore: vectorestore that helps to retreive document
    :return: Description
    :rtype: List[Document]

    """
    search_type = search_type.lower()

    chapter = filters.get("chapter") if filters else None
    verse = filters.get("verse") if filters else None
    language = filters.get("language", "english") if filters else "english"

    if search_type == "shloka":
        if chapter is not None and verse is not None:
            return get_shloka(chapter, verse)
        else :
            print(f"[WARN] Shloka route but chapter/verse missing. Falling back to semantic search.")
            search_type = "commentary"
    # semantic path
    retriever = get_retriever(
        k=3,
        route="commentary",
        filters={"language": language}
    )

    return retriever.invoke(question)


def extract_reference_regex(question: str) -> Tuple[Optional[int], Optional[int]]:
    q = question.lower()
    for pattern in REFERENCE_PATTERNS:
        match = re.search(pattern, q)
        if match:
            nums = match.groups()
            if "verse" in pattern and pattern.index("verse") < pattern.index("chapter"):
                verse, chapter = map(int, nums)
            else:
                chapter, verse = map(int, nums)

            if 1 <= chapter <= 18 and verse > 0:
                return chapter, verse

    return None, None