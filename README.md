

````markdown
# Hackathon Todo – Console Application

A Python-based console todo application built as **Phase I** of  
**“The Evolution of Todo – Hackathon II”**.  
The project focuses on spec-driven development, clean architecture, and an interactive CLI experience.

---

## Features

- Add tasks with a title and optional description  
- View all tasks in a formatted table  
- Filter tasks by status (pending / completed)  
- Update existing tasks  
- Delete tasks  
- Mark tasks as complete or incomplete  
- Interactive shell mode with persistent session  

---

## Prerequisites

- Python **3.13+**
- **uv** package manager

---

## Installation

```bash
git clone <repository-url>
cd hackathon-todo
uv sync
````

---

## Quick Start

### Option 1: Interactive Shell (Recommended)

```bash
uv run python -m hackathon_todo shell
```

Example session:

```
> add "Buy groceries" --description "Milk, eggs, bread"
Task created successfully (ID: 1)

> add "Call mom"
Task created successfully (ID: 2)

> list
┌────┬───────────────┬───────────┬─────────────────────┐
│ ID │ Title         │ Status    │ Created             │
├────┼───────────────┼───────────┼─────────────────────┤
│ 1  │ Buy groceries │ Pending   │ 2025-01-13 10:30    │
│ 2  │ Call mom      │ Pending   │ 2025-01-13 10:31    │
└────┴───────────────┴───────────┴─────────────────────┘

> complete 1
Task marked as complete

> list --status completed
┌────┬───────────────┬───────────┬─────────────────────┐
│ ID │ Title         │ Status    │ Created             │
├────┼───────────────┼───────────┼─────────────────────┤
│ 1  │ Buy groceries │ Done      │ 2025-01-13 10:30    │
└────┴───────────────┴───────────┴─────────────────────┘

> exit
Goodbye!
```

---

### Option 2: Single Command Mode

```bash
# Add a task
uv run python -m hackathon_todo add "Buy groceries" --description "Milk, eggs"

# List tasks
uv run python -m hackathon_todo list

# View a task
uv run python -m hackathon_todo view 1

# Update a task
uv run python -m hackathon_todo update 1 --title "New title"

# Mark as complete
uv run python -m hackathon_todo complete 1

# Delete a task
uv run python -m hackathon_todo delete 1
```

**Note:**
Single-command mode uses in-memory storage. Data resets between commands.
Use **shell mode** for a persistent session.

---

## Command Reference

| Command    | Usage                                               | Description             |
| ---------- | --------------------------------------------------- | ----------------------- |
| shell      | `shell`                                             | Start interactive shell |
| add        | `add "Title" [--description "Desc"]`                | Create a task           |
| list       | `list [--status pending\|completed]`                | List tasks              |
| view       | `view <id>`                                         | View task details       |
| update     | `update <id> [--title "New"] [--description "New"]` | Update a task           |
| complete   | `complete <id>`                                     | Mark task as completed  |
| uncomplete | `uncomplete <id>`                                   | Mark task as pending    |
| delete     | `delete <id>`                                       | Delete a task           |

---

## Project Structure

```
hackathon-todo/
├── src/
│   └── hackathon_todo/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli/
│       │   ├── app.py
│       │   ├── commands.py
│       │   └── display.py
│       ├── domain/
│       │   ├── models.py
│       │   └── exceptions.py
│       ├── services/
│       │   └── task_service.py
│       └── storage/
│           ├── base.py
│           └── memory.py
├── tests/
├── specs/
├── pyproject.toml
└── README.md
```

---

## Architecture Overview

```
PRESENTATION   : CLI (Click + Rich)
APPLICATION    : TaskService
DOMAIN         : Task model, validation, exceptions
INFRASTRUCTURE : In-memory storage
```

---

## Development

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/hackathon_todo

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
```

---

## Spec-Driven Development

This project follows **Spec-Kit Plus** methodology:

* `specs/todo-console-app/spec.md` – Requirements
* `specs/todo-console-app/plan.md` – Architecture plan
* `specs/todo-console-app/tasks.md` – Task breakdown

---

## License

MIT License

```


