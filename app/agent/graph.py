#graph.py
from langgraph.graph import StateGraph , START , END
from app.agent.state import SarthiState
from app.agent.nodes import (
    question_analysis,
    retrive_node ,
    answer_node,
    fall_back_node
)
def route(state:SarthiState)->str:
    docs = state["documents"]
    if docs:
        return "answer"
    return "fallback"

graph = StateGraph(SarthiState)
graph.add_node("question_analysis" , question_analysis)
graph.add_node("retrieve", retrive_node)
# graph.add_node("grade_docs", grade_documents_node) leaving for now ! 
graph.add_node("answer", answer_node)
graph.add_node("fallback", fall_back_node)


graph.add_edge(START , "question_analysis")
graph.add_edge("question_analysis" , "retrieve")
# graph.add_edge("retrieve" , "grade_docs")
graph.add_conditional_edges(
    "retrieve",
    route,
    {
        "answer" : "answer",
        "fallback":"fallback"
    }
)

graph.add_edge("answer" , END)
graph.add_edge("fallback" , END)

agent = graph.compile()
