from __future__ import annotations

import os
from typing import List, Dict, Any

from openai import OpenAI

from .storage import load_tasks, load_notes


# ------------------------------------------------------------
# Helper: Build client if API key exists
# ------------------------------------------------------------
def _get_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


# ------------------------------------------------------------
# Summarize all tasks + notes using AI (fallback if needed)
# ------------------------------------------------------------
def summarize_open_tasks_and_notes() -> str:
    data_tasks = load_tasks()      # dict with "tasks"
    data_notes = load_notes()      # dict with "notes"

    tasks = data_tasks.get("tasks", [])
    notes = data_notes.get("notes", [])

    if len(tasks) == 0 and len(notes) == 0:
        return "There are no tasks or notes to summarize."

    # Build text block
    text_block = "Tasks:\n"
    for t in tasks:
        if not isinstance(t, dict):
            continue
        status = "DONE" if t.get("done") else "OPEN"
        desc = t.get("description", "(no description)")
        text_block += f"- [{status}] {t.get('id')}: {desc}\n"

    text_block += "\nNotes:\n"
    for n in notes:
        if not isinstance(n, dict):
            continue
        title = n.get("title", "(untitled)")
        body = n.get("body", "")
        snippet = body[:60] + ("..." if len(body) > 60 else "")
        text_block += f"- {title}: {snippet}\n"

    # Attempt AI API call
    client = _get_client()

    if client:
        try:
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You summarize tasks and notes clearly."},
                    {"role": "user", "content": f"Summarize the following:\n\n{text_block}"}
                ],
                temperature=0.3,
            )
            return resp.choices[0].message.content
        except Exception:
            pass

    # Fallback summary
    open_tasks = sum(1 for t in tasks if isinstance(t, dict) and not t.get("done"))
    return (
        "⚠️ AI unavailable — using local summary.\n\n"
        f"- {open_tasks} open tasks\n"
        f"- {len(notes)} notes stored\n"
        "Try again later for full AI features."
    )


# ------------------------------------------------------------
# Create a simple plan for the day (AI + fallback)
# ------------------------------------------------------------
def suggest_plan_for_today() -> str:
    data_tasks = load_tasks()
    tasks = data_tasks.get("tasks", [])
    open_tasks = [t for t in tasks if isinstance(t, dict) and not t.get("done")]

    if len(open_tasks) == 0:
        return (
            "There are no open tasks.\n"
            "Your plan for today: relax, review notes, or add new tasks!"
        )

    # Build context
    text_block = "Open Tasks:\n"
    for t in open_tasks:
        desc = t.get("description", "(no description)")
        text_block += f"- {t.get('id')}: {desc}\n"

    # Try AI
    client = _get_client()

    if client:
        try:
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You create simple, effective daily plans."},
                    {"role": "user", "content": f"Create a plan for my day based on these tasks:\n\n{text_block}"}
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content
        except Exception:
            pass

    # Local fallback
    return (
        "⚠️ AI unavailable — using fallback plan.\n\n"
        "1. Complete the most important task first.\n"
        "2. Then do any task that takes under 5 minutes.\n"
        "3. Review remaining tasks and schedule them for tomorrow."
    )
