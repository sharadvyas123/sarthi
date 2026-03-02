#nodes.py
from app.agent.state import SarthiState , QueryAnalysis , ReferenceExtraction
from app.agent.tools import retrieve_gita_docs , extract_reference_regex
from langchain_core.prompts import ChatPromptTemplate
from app.config import SYSTEM_PROMPT_PATH, ANSWER_PROMPT_PATH
from langchain_ollama import ChatOllama
import os

MODEL_NAME = "llama3"
llm = ChatOllama(
    model=MODEL_NAME,
    base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    temperature=0
)

structured_llm = llm.with_structured_output(QueryAnalysis)
refrence_llm = llm.with_structured_output(ReferenceExtraction)

with open(str(SYSTEM_PROMPT_PATH), "r", encoding="utf-8") as f:
    system_prompt = f.read()

with open(str(ANSWER_PROMPT_PATH), "r", encoding="utf-8") as f:
    answer_prompt = f.read()

# -------------------------
# Retrieve Node
# -------------------------
def question_analysis(state: SarthiState) -> SarthiState:
    question = state["question"]

    result = structured_llm.invoke(
f"""
You are an expert query analyzer for a Bhagavad Gita AI assistant.

Your task is to analyze the user's question and return structured data.

Return ONLY structured output that follows the schema.

-------------------------------------

TASK 1 — Detect Language

Return:
- "hindi" → if the question is primarily written in Hindi or Devanagari script.
- "english" → otherwise.

-------------------------------------

TASK 2 — Detect Route

Return "shloka" ONLY if the user is requesting a SPECIFIC verse from the Bhagavad Gita.

The user MUST provide BOTH chapter AND verse numbers.

Examples of shloka queries:
- "Give me chapter 2 verse 47"
- "Show Bhagavad Gita 18.66"
- "What is shloka 4.7?"
- "BG 3.19"
- "गीता २.४७ बताओ"

IMPORTANT:
If the query asks about meaning, explanation, philosophy, karma yoga, dharma, bhakti, atman, etc — return "commentary".

Examples:
- "What is Karma Yoga?"
- "Explain Dharma"
- "Meaning of Nishkama Karma"
- "Why should Arjuna fight?"

🚨 CRITICAL RULE:
If there is ANY doubt → choose "commentary".

NEVER choose "shloka" unless BOTH chapter AND verse are present.

-------------------------------------

TASK 3 — Extract Chapter and Verse

ONLY when route = "shloka":

- Extract the numeric chapter and verse.
- Chapter must be between 1 and 18.
- Verse must be a positive integer.

If route = "commentary":
Return chapter = null  
Return verse = null

-------------------------------------

User Question:
{question}
"""
)
    
    chapter = result.chapter
    verse = result.verse
    

    if result.route == "shloka" and (chapter is None and verse is None):
        chapter , verse = extract_reference_regex(question)
    return {
        "route": result.route,
        "language": result.language,
        "verse":verse,
        "chapter":chapter
    }


# -------------------------
# Retrieve Node
# -------------------------
def retrive_node(state: SarthiState) -> SarthiState:
    question = state["question"]
    search_type = state.get("route","commentary")
    language = state.get("language","english")
    docs = retrieve_gita_docs(question, search_type=search_type, filters={"language" : language , "chapter":state["chapter"] , "verse" : state["verse"]})
    return {"documents":docs}


# -------------------------
# Grade Documents Node
# -------------------------
def grade_documents_node(state: SarthiState):

    question = state["question"]
    docs = state["documents"]

    if not docs:
        return {"documents": []}

    filtered_docs = []

    for doc in docs:

        grading_prompt = f"""
You are a strict relevance grader.

Question:
{question}

Document:
{doc.page_content}

Answer ONLY with:
YES
or
NO
"""
        response = llm.invoke(
            grading_prompt
        )

        verdict = response.content.strip().upper()

        if "YES" in verdict:
            filtered_docs.append(doc)

    return {"documents": filtered_docs}



# -------------------------
# Answer Node
# -------------------------
def answer_node(state: SarthiState)->SarthiState:

    docs = state["documents"]

    if not docs:
        return {
            "answer": "O seeker, this question is not answered directly in the sacred verses provided."
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", answer_prompt),
    ])

    formatted_prompt = prompt.format_prompt(
        context=context,
        question=state["question"]
    )

    response = llm.invoke(formatted_prompt)

    return {"answer": response.content}


# -------------------------
# Fall Back node
# -------------------------

def fall_back_node(state: SarthiState):

    return {
        "answer": (
            "O seeker, this question does not appear to be answered "
            "within the Bhagavad Gita. Seek truth through reflection "
            "and deeper inquiry."
        )
    }
