from __future__ import annotations

from typing import List, Dict, Any
from .storage import load_notes, save_notes


def _next_note_id(notes: List[Dict[str, Any]]) -> int:
    if not notes:
        return 1
    return max(n["id"] for n in notes) + 1


def add_note(title: str, body: str, tags: List[str] | None = None) -> Dict[str, Any]:
    data = load_notes()
    notes = data["notes"]

    nid = _next_note_id(notes)
    note = {
        "id": nid,
        "title": title or "",
        "body": body or "",
        "tags": tags or []
    }

    notes.append(note)
    save_notes(data)
    return note


def list_notes() -> List[Dict[str, Any]]:
    data = load_notes()
    return data["notes"]


def search_notes(query: str) -> List[Dict[str, Any]]:
    query = query.lower()
    data = load_notes()
    results = []
    for n in data["notes"]:
        if (
            query in n.get("title", "").lower()
            or query in n.get("body", "").lower()
            or any(query in tag.lower() for tag in n.get("tags", []))
        ):
            results.append(n)
    return results


def delete_note(note_id: int) -> bool:
    data = load_notes()
    notes = data["notes"]

    for i, n in enumerate(notes):
        if n["id"] == note_id:
            del notes[i]
            save_notes(data)
            return True

    return False
