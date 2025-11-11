#!/usr/bin/env python3
import json, pathlib

TASKS_FILE = pathlib.Path(__file__).resolve().parents[1] / "data" / "tasks.json"

def main():
    if not TASKS_FILE.exists():
        print("no tasks"); return
    db = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    tasks = db.get("tasks", [])
    if not tasks:
        print("no tasks"); return
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t['text']}  (created {t.get('created','')})")

if __name__ == "__main__":
    main()
