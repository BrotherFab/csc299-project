from __future__ import annotations

from typing import Any, Dict, List

from .storage import load_tasks, save_tasks


def _get_task_list() -> List[Dict[str, Any]]:
    """Load tasks list from storage (always returns a list)."""
    data = load_tasks()  # expects {"tasks": [...]}
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        tasks = []
    return tasks


def _save_task_list(tasks: List[Dict[str, Any]]) -> None:
    """Persist tasks list back to storage."""
    save_tasks({"tasks": tasks})


def _next_id(tasks: List[Dict[str, Any]]) -> int:
    """Compute the next task ID."""
    if not tasks:
        return 1
    return max(int(t.get("id", 0)) for t in tasks) + 1


def add_task(
    description: str,
    *,
    due: str | None = None,
    tags: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Create a new task and persist it.

    :param description: Text of the task (required, non-empty)
    :param due: Optional due date (stored as a simple string, e.g. '2025-12-01')
    :param tags: Optional list of tag strings (categories)
    """
    if description is None or not description.strip():
        raise ValueError("Task description cannot be empty.")

    tasks = _get_task_list()
    tid = _next_id(tasks)

    task = {
        "id": tid,
        "description": description.strip(),
        "status": "open",
        "done": False,
        "due": due,              # <--- NEW
        "tags": tags or [],      # <--- NEW
    }

    tasks.append(task)
    _save_task_list(tasks)
    return task


def list_tasks() -> List[Dict[str, Any]]:
    """Return all tasks as a list of dicts."""
    return _get_task_list()


def complete_task(task_id: int) -> bool:
    """Mark a task as done. Returns True if found, False otherwise."""
    tasks = _get_task_list()
    found = False

    for t in tasks:
        if int(t.get("id", 0)) == int(task_id):
            t["done"] = True
            t["status"] = "done"
            found = True
            break

    if found:
        _save_task_list(tasks)
    return found


def search_tasks(query: str) -> List[Dict[str, Any]]:
    """
    Case-insensitive search over description and tags.

    - Matches if query is contained in description
    - OR in any of the tags
    """
    q = (query or "").lower()
    tasks = _get_task_list()
    results: List[Dict[str, Any]] = []

    for t in tasks:
        desc = str(t.get("description", "")).lower()
        tag_list = [str(tag).lower() for tag in t.get("tags", [])]

        if q in desc or any(q in tag for tag in tag_list):
            results.append(t)

    return results


def delete_task(task_id: int) -> bool:
    """
    Delete a task by ID. Returns True if deleted, False if not found.
    """
    tasks = _get_task_list()
    new_tasks = [t for t in tasks if int(t.get("id", 0)) != int(task_id)]

    if len(new_tasks) == len(tasks):
        return False  # no deletion

    _save_task_list(new_tasks)
    return True
