from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import List, Optional

PRIORITIES = ("low", "medium", "high")

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    due: Optional[str] = None        # ISO date: YYYY-MM-DD
    priority: str = "medium"         # low | medium | high
    tags: List[str] = None           # list of strings
    completed: bool = False

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.priority not in PRIORITIES:
            self.priority = "medium"
        if self.due:
            # validate format early
            datetime.strptime(self.due, "%Y-%m-%d")

    def is_overdue(self) -> bool:
        if self.completed or not self.due:
            return False
        return date.today() > datetime.strptime(self.due, "%Y-%m-%d").date()

    def is_due_today(self) -> bool:
        if self.completed or not self.due:
            return False
        return date.today() == datetime.strptime(self.due, "%Y-%m-%d").date()

    def to_dict(self) -> dict:
        return asdict(self)
