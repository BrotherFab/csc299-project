# tasks4/tasks4/main.py
from __future__ import annotations
import os
from typing import Iterable, List
from openai import OpenAI

MODEL = "gpt-5-mini"  # per assignment

def summarize_paragraphs(paragraphs: Iterable[str]) -> List[str]:
    """
    Sends each paragraph to Chat Completions and returns a short-phrase summary for each.
    Each paragraph is summarized independently (no shared context).
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    summaries: List[str] = []

    for p in paragraphs:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You summarize tasks into short, action-oriented phrases (max ~8 words)."},
                {"role": "user", "content": f"Summarize this task into a short phrase:\n\n{p}"},
            ],
            temperature=0.2,
        )
        summaries.append(resp.choices[0].message.content.strip())
    return summaries

def main() -> None:
    # At least 2 sample paragraph-length descriptions (required)
    samples = [
        (
            "Meet with the facilities manager to review the new office "
            "floor plan, confirm desk allocations for the CS interns, "
            "and finalize the move-in checklist, including Wi-Fi setup, "
            "keycard access, and printer stations."
        ),
        (
            "Draft a two-page project brief outlining the PKMS roadmap, "
            "including milestones for data model changes, JSON-to-SQLite migration, "
            "and a testing plan with pytest fixtures and CI integration."
        ),
    ]

    summaries = summarize_paragraphs(samples)

    print("Task Summaries:")
    for i, s in enumerate(summaries, start=1):
        print(f"{i}. {s}")

if __name__ == "__main__":
    main()
