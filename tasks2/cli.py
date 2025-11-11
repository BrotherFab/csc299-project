#!/usr/bin/env python3
"""
tasks2 — Iterated Task Manager (CSC299)
Improvements over tasks1:
- Richer task model: id, title, description, due date, priority, tags, completed
- Filters: overdue, due today, by priority, by tag
- Mark complete
- Safer JSON storage with automatic file init
- Single-file CLI (no external deps)
"""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import uuid

DATA_PATH = Path("data")
STORE_FILE = DATA_PATH / "tasks2.json"

# ---------- Model ----------

PRIORITIES = ("low", "medium", "high")

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    due: Optional[str] = None         # ISO date "YYYY-MM-DD" or None
    priority: str = "medium"          # low | medium | high
    tags: List[str] = None            # list of strings
    completed: bool = False

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.priority not in PRIORITIES:
            self.priority = "medium"
        if self.due:
            # Validate date format early (raise ValueError if invalid)
            datetime.strptime(self.due, "%Y-%m-%d")

    def is_overdue(self) -> bool:
        if self.completed or not self.due:
            return False
        return date.today() > datetime.strptime(self.due, "%Y-%m-%d").date()

    def is_due_today(self) -> bool:
        if self.completed or not self.due:
            return False
        return date.today() == datetime.strptime(self.due, "%Y-%m-%d").date()

# ---------- Storage ----------

def _init_store() -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    if not STORE_FILE.exists():
        with STORE_FILE.open("w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

def _load_all() -> List[Task]:
    _init_store()
    with STORE_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Task(**t) for t in raw]

def _save_all(tasks: List[Task]) -> None:
    with STORE_FILE.open("w", encoding="utf-8") as f:
        json.dump([asdict(t) for t in tasks], f, indent=2)

# ---------- Helpers ----------

def _input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a value.")

def _input_optional(prompt: str) -> Optional[str]:
    s = input(prompt).strip()
    return s or None

def _input_priority() -> str:
    while True:
        s = input("Priority [low/medium/high] (default: medium): ").strip().lower()
        if not s:
            return "medium"
        if s in PRIORITIES:
            return s
        print("Invalid priority. Choose: low / medium / high.")

def _input_due() -> Optional[str]:
    s = input("Due date (YYYY-MM-DD, empty for none): ").strip()
    if not s:
        return None
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        print("Invalid date format. Example: 2025-11-03")
        return _input_due()

def _input_tags() -> List[str]:
    s = input("Tags (comma-separated, optional): ").strip()
    if not s:
        return []
    return [t.strip() for t in s.split(",") if t.strip()]

def _print_task(t: Task) -> None:
    flags = []
    if t.completed:
        flags.append("✓ done")
    if t.is_overdue():
        flags.append("OVERDUE")
    if t.is_due_today():
        flags.append("due today")
    flag_str = f" [{' | '.join(flags)}]" if flags else ""

    print(f"- {t.title}{flag_str}")
    print(f"  id: {t.id}")
    if t.description:
        print(f"  desc: {t.description}")
    if t.due:
        print(f"  due:  {t.due}")
    print(f"  prio: {t.priority}")
    if t.tags:
        print(f"  tags: {', '.join(t.tags)}")

def _choose_task(tasks: List[Task]) -> Optional[Task]:
    if not tasks:
        print("No tasks available.")
        return None
    print("\nSelect a task by number:")
    for idx, t in enumerate(tasks, start=1):
        mark = "✓" if t.completed else " "
        print(f"{idx:2d}. [{mark}] {t.title} (id: {t.id})")
    s = input("Number (or empty to cancel): ").strip()
    if not s:
        return None
    try:
        i = int(s)
        if 1 <= i <= len(tasks):
            return tasks[i-1]
    except ValueError:
        pass
    print("Invalid selection.")
    return None

# ---------- Actions ----------

def add_task() -> None:
    print("\nAdd Task")
    title = _input_nonempty("Title: ")
    desc = _input_optional("Description (optional): ") or ""
    due = _input_due()
    prio = _input_priority()
    tags = _input_tags()

    t = Task(
        id=str(uuid.uuid4())[:8],  # short id
        title=title,
        description=desc,
        due=due,
        priority=prio,
        tags=tags,
    )
    tasks = _load_all()
    tasks.append(t)
    _save_all(tasks)
    print("Task added.\n")

def list_tasks(filter_: str = "all", value: Optional[str] = None) -> None:
    tasks = _load_all()
    if filter_ == "overdue":
        tasks = [t for t in tasks if t.is_overdue()]
    elif filter_ == "today":
        tasks = [t for t in tasks if t.is_due_today()]
    elif filter_ == "priority" and value:
        tasks = [t for t in tasks if t.priority == value]
    elif filter_ == "tag" and value:
        tasks = [t for t in tasks if value in t.tags]
    elif filter_ == "open":
        tasks = [t for t in tasks if not t.completed]
    elif filter_ == "done":
        tasks = [t for t in tasks if t.completed]

    if not tasks:
        print("\nNo matching tasks.\n")
        return

    print()
    for t in tasks:
        _print_task(t)
    print()

def search_tasks() -> None:
    q = _input_nonempty("\nSearch term: ").lower()
    tasks = _load_all()
    hits = [
        t for t in tasks
        if q in t.title.lower()
        or q in (t.description or "").lower()
        or any(q in tag.lower() for tag in t.tags)
    ]
    if not hits:
        print("No results.\n")
        return
    print()
    for t in hits:
        _print_task(t)
    print()

def mark_complete() -> None:
    tasks = _load_all()
    t = _choose_task(tasks)
    if not t:
        return
    if t.completed:
        print("Already completed.\n")
        return
    t.completed = True
    _save_all(tasks)
    print("Marked complete.\n")

# ---------- Menu ----------

MENU = """
Task Manager (tasks2)
1) Add task
2) List all
3) List open
4) List done
5) List overdue
6) List due today
7) List by priority
8) List by tag
9) Search
10) Mark complete
q) Quit
"""

def main() -> None:
    _init_store()
    print(MENU)
    while True:
        choice = input("Select: ").strip().lower()
        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks("all")
        elif choice == "3":
            list_tasks("open")
        elif choice == "4":
            list_tasks("done")
        elif choice == "5":
            list_tasks("overdue")
        elif choice == "6":
            list_tasks("today")
        elif choice == "7":
            pr = input("Priority (low/medium/high): ").strip().lower()
            if pr not in PRIORITIES:
                print("Invalid priority.\n")
            else:
                list_tasks("priority", pr)
        elif choice == "8":
            tag = _input_nonempty("Tag: ")
            list_tasks("tag", tag)
        elif choice == "9":
            search_tasks()
        elif choice in ("q", "quit", "exit"):
            print("Bye!")
            break
        else:
            print("Unknown option.")
        print(MENU)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
