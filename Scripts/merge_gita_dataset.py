import json
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/"data"/"gita"

VERSE_FILE = DATA_DIR/"verse.json"
TRANSLATION_FILE = DATA_DIR/"translation.json"
COMMENTARY_FILE = DATA_DIR/"commentary.json"

OUTPUT_FILE = DATA_DIR / "gita_shlokas.json"


# print(BASE_DIR , DATA_DIR , VERSE_FILE , TRANSLATION_FILE , COMMENTARY_FILE) # to check weather the dir is ready or not ?? 


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)
    
def main():
    """
    This is the main function !!
    In this function we will transform the three diffrent files and merge those files into one file ! 

    the main ideas is to construct a file like this: 
    {
        verse : 1 ,
        shlok : "sholk in sanskrit ",
        and all diffrent featurer like translation , commentary etc.
    }
    """

    verses = load_json(VERSE_FILE)
    translations = load_json(TRANSLATION_FILE)
    commentaries  = load_json(COMMENTARY_FILE)

    merged = {}

     # -----------------------------
    # Base verses
    # -----------------------------
    for v in verses:
        vid = v["verse_id"]
        merged[vid] = {
            "chapter": v["chapter_number"],
            "verse": v["verse_number"],
            "verse_id": vid,
            "sanskrit": v["text"].strip(),
            "transliteration": v.get("transliteration", "").strip(),
            "word_meanings": v.get("word_meanings", "").strip(),
            "translations": defaultdict(list),
            "commentary": defaultdict(list),
        }

    # -----------------------------
    # Translations
    # -----------------------------
    for t in translations:
        vid = t["verse_id"]
        lang = t["lang"].lower()

        if vid not in merged:
            continue

        merged[vid]["translations"][lang].append({
            "author": t["authorName"],
            "text": t["description"].strip()
        })

    # -----------------------------
    # Commentary
    # -----------------------------
    for c in commentaries:
        vid = c["verse_id"]
        lang = c["lang"].lower()

        if vid not in merged:
            continue

        merged[vid]["commentary"][lang].append({
            "author": c["authorName"],
            "text": c["description"].strip()
        })
    
    final_data = []

    for v in merged.values():
        v["translations"] = dict(v["translations"])
        v["commentary"] = dict(v["commentary"])
        final_data.append(v)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Merged dataset saved to: {OUTPUT_FILE}")



if __name__ == "__main__":
    main()