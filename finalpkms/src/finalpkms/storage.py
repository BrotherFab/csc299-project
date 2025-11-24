from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

# Data directory lives alongside this package
DATA_DIR = (Path(__file__).resolve().parent.parent / "data").resolve()
NOTES_FILE = DATA_DIR / "notes.json"
TASKS_FILE = DATA_DIR / "tasks.json"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_data_dir()
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to read {path.name}: {e}") from e


def _save_json(path: Path, data: Dict[str, Any]) -> None:
    _ensure_data_dir()
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp.replace(path)


# -------- Tasks --------

def load_tasks() -> Dict[str, List[Dict[str, Any]]]:
    data = _load_json(TASKS_FILE, {"tasks": []})
    if "tasks" not in data or not isinstance(data["tasks"], list):
        data["tasks"] = []
    return data


def save_tasks(data: Dict[str, List[Dict[str, Any]]]) -> None:
    _save_json(TASKS_FILE, data)


# -------- Notes --------

def load_notes() -> Dict[str, List[Dict[str, Any]]]:
    data = _load_json(NOTES_FILE, {"notes": []})
    if "notes" not in data or not isinstance(data["notes"], list):
        data["notes"] = []
    return data


def save_notes(data: Dict[str, List[Dict[str, Any]]]) -> None:
    _save_json(NOTES_FILE, data)