from __future__ import annotations
import argparse
from pathlib import Path
from .store import (
    init_store, add_task, load_all, search,
    filter_tasks, mark_complete
)
from .model import PRIORITIES

# default data file: <repo-root>/data/tasks.json
DEFAULT_DATA_FILE = Path(__file__).resolve().parents[3] / "data" / "tasks.json"

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="tasks3", description="CSC299 tasks3 CLI")
    p.add_argument("-f", "--file", type=Path, default=DEFAULT_DATA_FILE, help="JSON file (default: data/tasks.json)")

    sub = p.add_subparsers(dest="cmd", required=True)

    sp_add = sub.add_parser("add", help="Add a new task")
    sp_add.add_argument("title")
    sp_add.add_argument("-d", "--description", default="")
    sp_add.add_argument("--due", help="YYYY-MM-DD", default=None)
    sp_add.add_argument("--priority", choices=PRIORITIES, default="medium")
    sp_add.add_argument("-t", "--tag", action="append", default=[])

    sub.add_parser("list", help="List all tasks")

    sp_f = sub.add_parser("filter", help="Filter tasks")
    sp_f.add_argument("mode", choices=["overdue", "today", "priority", "tag", "open", "done"])
    sp_f.add_argument("--value")

    sp_s = sub.add_parser("search", help="Search tasks by text")
    sp_s.add_argument("query")

    sp_c = sub.add_parser("complete", help="Mark a task complete by id")
    sp_c.add_argument("task_id")

    args = p.parse_args(argv)
    datafile: Path = args.file
    init_store(datafile)

    if args.cmd == "add":
        t = add_task(datafile, args.title, args.description, args.due, args.priority, args.tag)
        print(f"ADDED {t.id} :: {t.title} :: {t.tags}")
        return 0

    if args.cmd == "list":
        for t in load_all(datafile):
            print(f"{t.id} :: {t.title} :: {t.tags} :: prio={t.priority} :: due={t.due} :: done={t.completed}")
        return 0

    if args.cmd == "filter":
        for t in filter_tasks(datafile, args.mode, args.value):
            print(f"{t.id} :: {t.title} :: {t.tags} :: prio={t.priority} :: due={t.due} :: done={t.completed}")
        return 0

    if args.cmd == "search":
        for t in search(datafile, args.query):
            print(f"{t.id} :: {t.title} :: {t.tags} :: prio={t.priority} :: due={t.due} :: done={t.completed}")
        return 0

    if args.cmd == "complete":
        ok = mark_complete(datafile, args.task_id)
        print("OK" if ok else "NOT FOUND")
        return 0 if ok else 1

    p.error("unknown command")
    return 2
