sarthi/
├── app/
│   ├── agent/                 # LangGraph brain
│   │   ├── __init__.py
│   │   ├── graph.py           # graph construction
│   │   ├── nodes.py           # retrieve, answer, reflect nodes
│   │   ├── state.py           # graph state schema
│   │   └── tools.py           # retriever, shloka lookup tools
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── loader.py          # load Gita PDFs / JSON
│   │   ├── splitter.py        # chunking strategy
│   │   ├── embeddings.py      # embedding model
│   │   ├── vectorstore.py     # Chroma DB logic
│   │   └── retriever.py       # semantic + verse retrieval
│   │
│   ├── prompts/
│   │   ├── system_prompt.txt  # Krishna-like behavior
│   │   ├── answer_prompt.txt  # how to answer life questions
│   │   └── shloka_prompt.txt  # verse explanation format
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py            # FastAPI / Streamlit endpoint
│   │
│   └── config.py              # model, paths, constants
│
├── data/
│   ├── gita/
│   │   ├── bhagavad_gita.pdf
│   │   ├── gita_shlokas.json  # chapter, verse, meaning
│   │   └── translations/
│   │       ├── english.json
│   │       └── hindi.json
│
├── chroma_db/                 # persisted vector DB
│
├── .env
├── requirements.txt
├── langgraph.json
└── run.py                     # entry point
