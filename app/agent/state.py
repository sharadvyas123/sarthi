from typing import List, Optional, TypedDict , Literal
from langchain_core.documents import Document
from pydantic import BaseModel

class SarthiState(TypedDict):
    question: str
    documents: List[Document]
    answer: Optional[str]
    route : str
    language : str
    verse : int
    chapter:int

class QueryAnalysis(BaseModel):
    route : Literal["shloka" , "commentary"]
    language : Literal["hindi" , "english"]
    chapter: Optional[int] = None
    verse: Optional[int] = None
class ReferenceExtraction(BaseModel):
    chapter: Optional[int] = None
    verse: Optional[int] = None
