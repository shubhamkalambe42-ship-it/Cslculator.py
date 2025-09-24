Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
#!/usr/bin/env python3
"""
Console To-Do List Application
Save this file as todo.py and run: python todo.py
"""

import json
import os
import datetime
from typing import List, Optional

DATA_FILE = "todos.json"


class TodoItem:
    def __init__(self, title: str, notes: str = "", priority: int = 3,
                 due: Optional[str] = None, done: bool = False, created_at: Optional[str] = None):
        self.title = title.strip()
        self.notes = notes.strip()
        self.priority = int(priority)
        self.due = due.strip() if due else None  # store as ISO date string YYYY-MM-DD or None
        self.done = bool(done)
        self.created_at = created_at or datetime.datetime.now().isoformat()

    def to_dict(self):
        return {
            "title": self.title,
            "notes": self.notes,
            "priority": self.priority,
            "due": self.due,
            "done": self.done,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(d):
        return TodoItem(
            title=d.get("title", ""),
            notes=d.get("notes", ""),
            priority=d.get("priority", 3),
            due=d.get("due"),
            done=d.get("done", False),
            created_at=d.get("created_at"),
        )

    def __repr__(self):
        status = "✓" if self.done else " "
        due = f" | due: {self.due}" if self.due else ""
        pr = f"P{self.priority}"
        return f"[{status}] {self.title} ({pr}){due}" + (f"\n    {self.notes}" if self.notes else "")


class TodoList:
    def __init__(self):
        self.items: List[TodoItem] = []
        self.load()

    def add(self, item: TodoItem):
        self.items.append(item)
        self.save()

    def list(self, show="all"):
        if show == "pending":
            items = [i for i in self.items if not i.done]
        elif show == "done":
            items = [i for i in self.items if i.done]
        else:
            items = list(self.items)
        # sort by done, then priority, then due date (None goes last), then created_at
        def sort_key(it: TodoItem):
            due_dt = datetime.datetime.max
            if it.due:
                try:
                    due_dt = datetime.datetime.fromisoformat(it.due)
                except ValueError:
                    pass
            return (it.done, it.priority, due_dt, it.created_at)
        items.sort(key=sort_key)
        return items

    def mark(self, index: int, done: bool = True):
        if 0 <= index < len(self.items):
            self.items[index].done = done
            self.save()
            return True
        return False

    def delete(self, index: int):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.save()
            return True
        return False

    def edit(self, index: int, title=None, notes=None, priority=None, due=None):
        if 0 <= index < len(self.items):
            it = self.items[index]
            if title is not None:
                it.title = title.strip()
            if notes is not None:
                it.notes = notes.strip()
            if priority is not None:
                it.priority = int(priority)
            if due is not None:
                it.due = due.strip() if due else None
            self.save()
            return True
        return False

    def search(self, term: str):
        term = term.lower()
        return [i for i in self.items if term in i.title.lower() or term in i.notes.lower()]

    def save(self):
        data = [i.to_dict() for i in self.items]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [TodoItem.from_dict(d) for d in data]
            except Exception:
                print("Warning: failed to load data file; starting fresh.")
                self.items = []
        else:
            self.items = []


def parse_date_input(s: str) -> Optional[str]:
    s = s.strip()
    if not s:
        return None
    # Accept YYYY-MM-DD or common variants; try to parse
    try:
        dt = datetime.date.fromisoformat(s)
        return dt.isoformat()
    except Exception:
        # try some flexible parsing: dd-mm-yyyy or dd/mm/yyyy
        for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                dt = datetime.datetime.strptime(s, fmt).date()
                return dt.isoformat()
            except Exception:
                pass
    print("Warning: could not parse due date. Store as raw string.")
    return s


def print_help():
    print("""
Commands:
  add             - Add a new task
  list [all|pending|done]
                  - Show tasks (default: all)
  done <#>        - Mark task number # as done
  undone <#>      - Mark task # as not done
  edit <#>        - Edit task #
  del <#>         - Delete task #
  search <term>   - Search tasks by keyword
  clear           - Delete ALL tasks (confirmation required)
  help            - Show this help
  exit / quit     - Exit program
Notes:
  - Task numbers shown by 'list' are 1-based.
  - Priority is 1 (highest) to 5 (lowest). Default is 3.
  - Due date recommended format: YYYY-MM-DD (e.g. 2025-09-23)
""")


def main():
    todo = TodoList()
    print("Welcome to To-Do (console). Type 'help' for commands.")
    while True:
        try:
            cmd = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        if not cmd:
            continue
        parts = cmd.split()
        action = parts[0].lower()

        if action in ("exit", "quit"):
            print("Goodbye!")
            break
        elif action == "help":
            print_help()
        elif action == "add":
            title = input("Title: ").strip()
            if not title:
                print("Aborted: title cannot be empty.")
                continue
            notes = input("Notes (optional): ").strip()
            pr = input("Priority (1-5, default 3): ").strip() or "3"
            try:
                pr_int = int(pr)
                if not (1 <= pr_int <= 5):
                    raise ValueError
            except ValueError:
                print("Invalid priority, using 3.")
                pr_int = 3
            due_raw = input("Due date (YYYY-MM-DD) optional: ").strip()
            due = parse_date_input(due_raw) if due_raw else None
            item = TodoItem(title=title, notes=notes, priority=pr_int, due=due)
            todo.add(item)
            print("Added.")
        elif action == "list":
            show = "all"
            if len(parts) > 1:
                arg = parts[1].lower()
                if arg in ("all", "pending", "done"):
                    show = arg
                else:
                    print("Unknown list option. Use all|pending|done. Defaulting to all.")
            items = todo.list(show=show)
            if not items:
                print("(no tasks)")
                continue
            for idx, it in enumerate(items, start=1):
                status = "✓" if it.done else " "
                due = f" | due: {it.due}" if it.due else ""
                print(f"{idx}. [{status}] {it.title} (P{it.priority}){due}")
                if it.notes:
                    print(f"    {it.notes}")
        elif action in ("done", "undone", "del", "edit"):
            if len(parts) < 2:
                print(f"Usage: {action} <task-number-as-listed>")
                continue
            try:
                idx = int(parts[1]) - 1
            except ValueError:
                print("Task number must be an integer.")
                continue
            items = todo.list()  # list in sorted order; mapping to index
            if idx < 0 or idx >= len(items):
                print("Invalid task number.")
                continue
            # Need to find the actual index in underlying storage
            target_item = items[idx]
            real_index = todo.items.index(target_item)
            if action == "done":
                todo.mark(real_index, True)
                print("Marked done.")
            elif action == "undone":
                todo.mark(real_index, False)
                print("Marked undone.")
            elif action == "del":
                confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()
                if confirm == "y":
                    todo.delete(real_index)
                    print("Deleted.")
                else:
                    print("Cancelled.")
            elif action == "edit":
                print("Leave a field blank to keep current value.")
                cur = todo.items[real_index]
                new_title = input(f"Title [{cur.title}]: ").strip() or None
                new_notes = input(f"Notes [{cur.notes}]: ").strip() or None
                new_pr = input(f"Priority [{cur.priority}]: ").strip() or None
                new_due_raw = input(f"Due [{cur.due or ''}]: ").strip()
                new_due = parse_date_input(new_due_raw) if new_due_raw != "" else None
...                 # For fields where user pressed blank -> keep, so pass None
...                 todo.edit(real_index,
...                           title=new_title if new_title is not None else None,
...                           notes=new_notes if new_notes is not None else None,
...                           priority=int(new_pr) if new_pr and new_pr.isdigit() else None,
...                           due=new_due if new_due_raw != "" else None)
...                 print("Edited.")
...         elif action == "search":
...             if len(parts) < 2:
...                 print("Usage: search <term>")
...                 continue
...             term = " ".join(parts[1:])
...             found = todo.search(term)
...             if not found:
...                 print("No matches.")
...             else:
...                 for idx, it in enumerate(found, start=1):
...                     st = "✓" if it.done else " "
...                     due = f" | due: {it.due}" if it.due else ""
...                     print(f"{idx}. [{st}] {it.title} (P{it.priority}){due}")
...                     if it.notes:
...                         print(f"    {it.notes}")
...         elif action == "clear":
...             confirm = input("Delete ALL tasks? This cannot be undone. Type DELETE to confirm: ")
...             if confirm == "DELETE":
...                 todo.items = []
...                 todo.save()
...                 print("All tasks removed.")
...             else:
...                 print("Cancelled.")
...         else:
...             print("Unknown command. Type 'help' to see commands.")
... 
... 
... if __name__ == "__main__":
...     main()
