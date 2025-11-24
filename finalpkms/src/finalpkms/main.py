from __future__ import annotations

import shlex

from .tasks import add_task, list_tasks, complete_task, search_tasks, delete_task
from .notes import add_note, list_notes, search_notes, delete_note
from .agents import summarize_open_tasks_and_notes, suggest_plan_for_today


HELP_TEXT = """
Commands:

  help                     Show this help.
  quit / exit              Exit the program.

  add task [desc]          Add a new task. If desc omitted, you will be prompted.
  list tasks               List all tasks.
  done <id>                Mark task with given ID as done.
  search tasks <query>     Search tasks by text.
  delete task <id>         Delete task by ID.

  add note                 Add a new note (interactive).
  list notes               List all notes.
  search notes <query>     Search notes by text.
  delete note <id>         Delete note by ID.

  agent summary            AI: summarize current tasks + notes.
  agent plan               AI: suggest a plan for today based on open tasks.
""".strip()


def _print_task(task: dict) -> None:
    tags = ", ".join(task.get("tags") or [])
    print(
        f"[#{task['id']}] {task['description']} "
        f"(status={task.get('status')}, due={task.get('due')}, tags={tags})"
    )


def _print_note(note: dict) -> None:
    tags = ", ".join(note.get("tags") or [])
    title = note.get("title") or "(no title)"
    print(f"[#{note['id']}] {title} (tags={tags})")
    if note.get("body"):
        print("    " + note["body"].replace("\n", "\n    "))


def main() -> None:
    print("=== CSC299 Final PKMS ===")
    print("Type 'help' for commands. 'quit' to exit.\n")

    while True:
        try:
            raw = input("pkms> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        try:
            parts = shlex.split(raw)
        except ValueError as e:
            print(f"Could not parse command: {e}")
            continue

        cmd = parts[0].lower()
        args = parts[1:]

        # Exit / help
        if cmd in {"quit", "exit", "q"}:
            print("Goodbye.")
            break
        if cmd == "help":
            print(HELP_TEXT)
            continue

        # ---- Task commands ----
        # ---- Task commands ----
        if cmd == "add" and len(args) >= 1 and args[0] == "task":
            # Description can come from the command line or prompt
            desc = " ".join(args[1:]).strip()
            if not desc:
                desc = input("Task description: ").strip()

            # Ask for optional due date
            due = input("Due date (optional, e.g., 2025-12-01): ").strip()
            if not due:
                due = None

            # Ask for optional tags
            tags_input = input("Tags (comma-separated, optional): ").strip()
            tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []

            try:
                task = add_task(desc, due=due, tags=tags)
                print("Added task:")
                _print_task(task)
            except ValueError as e:
                print(f"Error: {e}")
            continue

        if cmd == "list" and len(args) == 1 and args[0] == "tasks":
            tasks = list_tasks()
            if not tasks:
                print("No tasks yet.")
            else:
                for t in tasks:
                    _print_task(t)
            continue

        if cmd == "done" and len(args) == 1:
            try:
                tid = int(args[0])
            except ValueError:
                print("Usage: done <task-id>")
                continue
            if complete_task(tid):
                print(f"Marked task #{tid} as done.")
            else:
                print(f"No task found with id {tid}.")
            continue

        if cmd == "search" and len(args) >= 2 and args[0] == "tasks":
            query = " ".join(args[1:])
            results = search_tasks(query)
            if not results:
                print("No matching tasks.")
            else:
                for t in results:
                    _print_task(t)
            continue

        if cmd == "delete" and len(args) == 2 and args[0] == "task":
            try:
                tid = int(args[1])
            except ValueError:
                print("Usage: delete task <id>")
                continue
            if delete_task(tid):
                print(f"Deleted task #{tid}.")
            else:
                print("No such task.")
            continue

        if cmd == "list" and len(args) == 1 and args[0] == "notes":
            notes = list_notes()
            if not notes:
                print("No notes yet.")
            else:
                for n in notes:
                    _print_note(n)
            continue

        if cmd == "search" and len(args) >= 2 and args[0] == "notes":
            query = " ".join(args[1:])
            results = search_notes(query)
            if not results:
                print("No matching notes.")
            else:
                for n in results:
                    _print_note(n)
            continue

        if cmd == "delete" and len(args) == 2 and args[0] == "note":
            try:
                nid = int(args[1])
            except ValueError:
                print("Usage: delete note <id>")
                continue
            if delete_note(nid):
                print(f"Deleted note #{nid}.")
            else:
                print("No such note.")
            continue

        # ---- Agent commands ----
        if cmd == "agent" and len(args) == 1 and args[0] == "summary":
            print("Running AI summary agent...\n")
            text = summarize_open_tasks_and_notes()
            print(text)
            continue

        if cmd == "agent" and len(args) == 1 and args[0] == "plan":
            print("Running AI planning agent...\n")
            text = suggest_plan_for_today()
            print(text)
            continue

        print("Unknown command. Type 'help' for list of commands.")
