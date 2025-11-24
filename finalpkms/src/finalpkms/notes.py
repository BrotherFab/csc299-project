from __future__ import annotations

from typing import Any, Dict, List

from .storage import load_notes as _load_notes_dict, save_notes as _save_notes_dict


def _get_notes() -> List[Dict[str, Any]]:
    """Load notes list from storage dict."""
    data = _load_notes_dict()
    return data.get("notes", [])


def _save_notes(notes: List[Dict[str, Any]]) -> None:
    """Save notes list back into storage dict."""
    _save_notes_dict({"notes": notes})


def list_notes() -> List[Dict[str, Any]]:
    """Return all notes as a list of dicts."""
    return _get_notes()


def _next_id(notes: List[Dict[str, Any]]) -> int:
    """Compute next note ID."""
    return max((n.get("id", 0) for n in notes), default=0) + 1


def add_note(title: str, body: str) -> Dict[str, Any]:
    """Add a new note with title + body."""
    body_text = (body or "").strip()
    title_text = (title or "").strip()

    if not body_text:
        raise ValueError("Note body cannot be empty.")

    notes = _get_notes()
    nid = _next_id(notes)

    note = {
        "id": nid,
        "title": title_text or f"Note {nid}",
        "body": body_text,
        "tags": [],
    }

    notes.append(note)
    _save_notes(notes)
    return note


def search_notes(query: str) -> List[Dict[str, Any]]:
    """Case-insensitive search in title and body."""
    q = (query or "").lower()
    if not q:
        return []

    notes = _get_notes()
    results: List[Dict[str, Any]] = []

    for n in notes:
        title = str(n.get("title", "")).lower()
        body = str(n.get("body", "")).lower()
        if q in title or q in body:
            results.append(n)

    return results


def delete_note(note_id: int) -> bool:
    """Delete a note by ID. Returns True if something was deleted."""
    notes = _get_notes()
    new_notes = [n for n in notes if n.get("id") != note_id]

    if len(new_notes) == len(notes):
        return False

    _save_notes(new_notes)
    return True
