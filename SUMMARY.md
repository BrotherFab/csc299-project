# SUMMARY

## Overview of Development Process

For this final project, I built a Personal Knowledge Management System (PKMS) with a task manager, notes system, AI-assisted agents, and a terminal chat-style interface. The project evolved through multiple prototypes (tasks1–tasks5) before producing the final version in the `finalpkms` directory.

Throughout the project, I used several AI coding tools, each serving a different purpose and contributing to the overall development.

---

## Use of AI Coding Assistants

### **ChatGPT**
ChatGPT was my primary day-to-day development assistant.  
I used it for:
- Writing initial prototypes  
- Understanding errors  
- Debugging broken logic  
- Explaining Python and CLI behavior  
- Designing the structure of the PKMS  
- Generating unit tests and correcting failing ones  
- Fixing tricky bugs that Copilot or Claude couldn’t figure out  

ChatGPT also helped me understand PowerShell commands, uv behavior, and Python packaging. It ended up being the most consistently useful tool because it always let me verify code line-by-line.

### **Claude (Anthropic)**
Claude was especially helpful for:
- High-level discussions about architecture  
- Understanding lecture material  
- Talking through why certain designs work better than others  
- Brainstorming features like agents, planning, and note structures  

Claude was excellent for “big picture thinking,” though less useful than ChatGPT for the actual implementation details.

### **GitHub Copilot**
Copilot was used heavily during the **tasks5** phase when we worked with GitHub’s **spec-kit**. I relied on Copilot for:
- Autocomplete inside VS Code  
- Filling out boilerplate code  
- Scaffolding functions quickly  
- Suggesting small helper functions when my own logic was clear  

It was good for speed, but not always accurate — sometimes it hallucinated outdated syntax or paths, especially with uv-based projects.

### **Windsurf**
I used Windsurf mainly for:
- Autocomplete  
- Navigating files faster  
- Lightweight inline suggestions  

It helped with flow, especially during the rapid iteration of the final PKMS code.

---

## What Worked Well

- **Iterating with LLMs** let me build each version of the system both quickly and safely.
- Using ChatGPT for debugging saved hours — especially for import errors, JSON layout issues, and incorrect directory paths.
- The chat-style interface turned out extremely flexible and intuitive.
- AI agents (summary + day planning) worked well once the OpenAI API key issues were resolved.
- The final version of the PKMS is stable, has optional tags and due dates, supports deleting tasks/notes, and provides meaningful AI summaries.

---

## What Didn’t Work or Caused Problems

- **LLMs didn’t always know the newest uv or Python packaging commands.**  
  I had to re-try multiple instructions because some suggestions were outdated.
- **OpenAI token issues** caused the biggest delays.  
  Even after setting the API key, I kept hitting insufficient quota errors and needed to manually verify billing + project setup.
- **File paths confused several models** (ChatGPT, Claude, Copilot).  
  Some tried to write data to nonexistent directories, or assumed I was using a different project layout.
- **Spec-kit documentation is sparse**, so combining Copilot + ChatGPT was necessary to understand how to use the generated structure.

---

## Overall Reflection

Using multiple AI tools actually made me understand Python, CLI workflows, uv, ChatGPT’s API, and Git much better.  
The final PKMS represents a real combination of:
- human-guided design  
- AI-assisted debugging  
- iterative prototyping  
- and a layered understanding of software development  

The system now supports tasks, notes, searching, deletion, due dates, tags, and AI-based helpers. The process taught me to verify everything carefully and not rely blindly on any one assistant.

