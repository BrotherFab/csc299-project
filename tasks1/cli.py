import json
from pathlib import Path

# Define where the tasks are stored
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_tasks():
    """Load all tasks from the JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Save all tasks to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task():
    """Add a new task."""
    title = input("Enter task title: ").strip()
    description = input("Enter task description (optional): ").strip()
    tasks = load_tasks()
    tasks.append({"title": title, "description": description})
    save_tasks(tasks)
    print("✅ Task added!\n")


def list_tasks():
    """List all stored tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.\n")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']} - {task.get('description', '')}")
    print()


def search_tasks():
    """Search tasks by keyword."""
    keyword = input("Enter keyword to search: ").strip().lower()
    tasks = load_tasks()
    results = [
        t for t in tasks if keyword in t["title"].lower() or keyword in t.get("description", "").lower()
    ]
    if not results:
        print("No matching tasks.\n")
        return
    print("\nSearch Results:")
    for i, task in enumerate(results, 1):
        print(f"{i}. {task['title']} - {task.get('description', '')}")
    print()


def main():
    """Main menu for the task manager."""
    while True:
        print("Task Manager Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Search Tasks")
        print("4. Quit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            search_tasks()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
