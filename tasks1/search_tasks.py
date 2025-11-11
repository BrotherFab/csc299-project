#!/usr/bin/env python3
import json, sys, pathlib

TASKS_FILE = pathlib.Path(__file__).resolve().parents[1] / "data" / "tasks.json"

def main():
    if len(sys.argv) < 2:
        print("usage: python tasks1/search_tasks.py <keyword>")
        sys.exit(1)
    q = " ".join(sys.argv[1:]).strip().lower()
    if not TASKS_FILE.exists():
        print("no matches"); return
    db = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    hits = [t for t in db.get("tasks", []) if q in t["text"].lower()]
    if not hits:
        print("no matches"); return
    for i, t in enumerate(hits, 1):
        print(f"{i}. {t['text']}")

if __name__ == "__main__":
    main()
