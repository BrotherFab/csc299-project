from __future__ import annotations
import json
import uuid
from pathlib import Path
from typing import List, Optional
from .model import Task, PRIORITIES

def init_store(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")

def load_all(path: Path) -> List[Task]:
    init_store(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Task(**t) for t in raw]

def save_all(path: Path, tasks: List[Task]) -> None:
    path.write_text(
        json.dumps([t.to_dict() for t in tasks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

def add_task(
    path: Path,
    title: str,
    description: str = "",
    due: Optional[str] = None,
    priority: str = "medium",
    tags: Optional[list[str]] = None,
) -> Task:
    if priority not in PRIORITIES:
        priority = "medium"
    t = Task(
        id=str(uuid.uuid4())[:8],
        title=title,
        description=description or "",
        due=due,
        priority=priority,
        tags=tags or [],
    )
    tasks = load_all(path)
    tasks.append(t)
    save_all(path, tasks)
    return t

def search(path: Path, query: str) -> List[Task]:
    q = query.lower()
    hits = []
    for t in load_all(path):
        hay = [
            t.title.lower(),
            (t.description or "").lower(),
            *[tag.lower() for tag in t.tags],
        ]
        if any(q in part for part in hay):
            hits.append(t)
    return hits

def filter_tasks(path: Path, mode: str, value: Optional[str] = None) -> List[Task]:
    tasks = load_all(path)
    if mode == "overdue":
        return [t for t in tasks if t.is_overdue()]
    if mode == "today":
        return [t for t in tasks if t.is_due_today()]
    if mode == "priority" and value:
        return [t for t in tasks if t.priority == value]
    if mode == "tag" and value:
        return [t for t in tasks if value in t.tags]
    if mode == "open":
        return [t for t in tasks if not t.completed]
    if mode == "done":
        return [t for t in tasks if t.completed]
    return tasks

def mark_complete(path: Path, task_id: str) -> bool:
    tasks = load_all(path)
    found = False
    for t in tasks:
        if t.id == task_id:
            if not t.completed:
                t.completed = True
            found = True
            break
    if found:
        save_all(path, tasks)
    return found
