from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GITA_DATA_PATH = BASE_DIR / "data" / "gita" / "gita_shlokas.json"
CHROMA_PATH= BASE_DIR / "chroma_db"
SYSTEM_PROMPT_PATH = BASE_DIR / "app" / "prompts" / "system_prompt.txt"
ANSWER_PROMPT_PATH = BASE_DIR / "app" / "prompts" / "answer_prompt.txt"