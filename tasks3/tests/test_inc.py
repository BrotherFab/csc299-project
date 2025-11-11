# tasks3/tests/test_inc.py
from pathlib import Path
from datetime import date, timedelta

from tasks3 import inc
from tasks3.store import (
    add_task,
    load_all,
    save_all,
    search,
    filter_tasks,
    mark_complete,
)
from tasks3.cli import main as cli_main


def test_inc():
    assert inc(5) == 6
    assert inc(0) == 1
    assert inc(-3) == -2


def test_add_and_persist(tmp_path: Path):
    file = tmp_path / "tasks.json"
    created = add_task(file, "Write CSC299 report", priority="high", tags=["school"])
    assert created.title == "Write CSC299 report"
    assert created.priority == "high"
    assert isinstance(created.id, str) and created.id  # non-empty id

    tasks = load_all(file)
    # persisted?
    assert any(t.id == created.id for t in tasks)


def test_mark_complete_and_filters(tmp_path: Path):
    file = tmp_path / "tasks.json"
    a = add_task(file, "Task A")
    b = add_task(file, "Task B")
    # both start open
    assert len(filter_tasks(file, "open")) == 2
    assert len(filter_tasks(file, "done")) == 0

    # complete one
    ok = mark_complete(file, a.id)
    assert ok is True

    open_tasks = filter_tasks(file, "open")
    done_tasks = filter_tasks(file, "done")
    assert {t.id for t in open_tasks} == {b.id}
    assert {t.id for t in done_tasks} == {a.id}


def test_search(tmp_path: Path):
    file = tmp_path / "tasks.json"
    # Seed via add_task (returns Task and persists to file)
    _a = add_task(file, "Buy milk")
    _b = add_task(file, "Write CSC299 report", tags=["School"])

    # search is case-insensitive over title/desc/tags
    hits = search(file, "cSc299")
    assert len(hits) == 1
    assert hits[0].title == "Write CSC299 report"



def test_due_today_overdue_and_cli_list(tmp_path: Path, capsys):
    file = tmp_path / "tasks.json"
    today = date.today().strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    t_today = add_task(file, "Due now", due=today)
    t_past = add_task(file, "Due yesterday", due=yesterday)

    due_today = filter_tasks(file, "today")
    overdue = filter_tasks(file, "overdue")

    assert {t.id for t in due_today} == {t_today.id}
    assert {t.id for t in overdue} == {t_past.id}

    # Exercise the CLI "list" output (call cli_main directly with argv)
    # NOTE: We include --file to keep tests isolated in tmp_path.
    rc = cli_main(["--file", str(file), "list"])
    captured = capsys.readouterr().out
    assert rc == 0
    # Should list both tasks with their ids/titles somewhere in output
    assert t_today.id in captured and "Due now" in captured
    assert t_past.id in captured and "Due yesterday" in captured
