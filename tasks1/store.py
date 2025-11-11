#!/usr/bin/env python3
import json, sys, pathlib, datetime

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)
TASKS_FILE = DATA_DIR / "tasks.json"

def load():
    if TASKS_FILE.exists():
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    return {"tasks": []}

def save(db):
    TASKS_FILE.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    if len(sys.argv) < 2:
        print("usage: python tasks1/store.py <task text>")
        sys.exit(1)
    text = " ".join(sys.argv[1:]).strip()
    if not text:
        print("error: empty task"); sys.exit(1)

    db = load()
    db["tasks"].append({
        "text": text,
        "created": datetime.datetime.now().isoformat(timespec="seconds")
    })
    save(db)
    print(f"stored task: {text}")

if __name__ == "__main__":
    main()
