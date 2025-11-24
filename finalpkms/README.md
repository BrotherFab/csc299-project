# Final PKMS & Task Manager — CSC299 Final Project

This is the final Personal Knowledge Management System (PKMS) and Task Manager developed for **CSC299**.  
It is a terminal-based application written in **Python**, using **JSON storage** and optional **OpenAI-powered AI agents** for summaries and planning.

The system provides:
- A task manager with due dates, tags/categories, search, completion, and deletion.
- A note-taking system with titles, bodies, tags, search, and deletion.
- An interactive REPL-style chat interface.
- Optional AI agents:
  - **Agent Summary** — Summarizes tasks + notes.
  - **Agent Plan** — Suggests a daily plan.
- Fully portable across Windows, Mac, and Linux.
- All state saved in JSON files under `data/`.

---

## 📦 Installation

From inside the `finalpkms` directory:

```sh
uv sync

This creates the virtual environment and installs dependencies from pyproject.toml.

Run the program with:

uv run finalpkms

You should see:
=== CSC299 Final PKMS ===
Type 'help' for commands. 'quit' to exit.


AI features require an API key.

In PowerShell:

$env:OPENAI_API_KEY = "your-key-here"

uv run python -c "from openai import OpenAI; c=OpenAI(); print(c.chat.completions.create(model='gpt-4.1-mini', messages=[{'role':'user','content':'hi'}]).choices[0].message.content)"

Without an API key, the system still works using local fallback summaries/plans.

🧠 Features
✅ Task Management

Add a task with:
description
optional due date
optional tags
List all tasks
Search tasks by text
Mark as done
Delete tasks
JSON persistence

📝 Notes
Add notes interactively
List all notes
Search notes
Delete notes
JSON persistence

🤖 AI Agents (optional)

agent summary
Summarizes your tasks + notes.
agent plan
Generates a daily productivity plan.

If the API is unavailable, rate-limited, or missing, the app automatically uses non-AI fallback behavior.

At the pkms> prompt:

help                     Show this help text
quit / exit              Exit the program

add task [desc]          Add a new task (prompts for due date + tags)
list tasks               View all tasks
done <id>                Mark a task as completed
search tasks <query>     Search tasks
delete task <id>         Delete a task

add note                 Add a new note interactively
list notes               View all notes
search notes <query>     Search notes
delete note <id>         Delete a note

agent summary            AI-based summary of tasks + notes
agent plan               AI-based plan for the day
