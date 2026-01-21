from typing import List, TypedDict

class SarthiState(TypedDict):
    question: str
    retrieved_shlokas: List[str]
    answer: str
