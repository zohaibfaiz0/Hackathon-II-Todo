---
id: 1
title: fix-cli-command-structure
stage: general
date: 2026-01-13
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: AA
command: "Fix the CLI in src/hackathon_todo/cli/commands.py"
labels: ["cli", "commands", "refactor"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - C:/Users/AA/Desktop/sp+/hackathon-todo/src/hackathon_todo/cli/commands.py
tests:
 - none
---

## Prompt

Fix the CLI in src/hackathon_todo/cli/commands.py

Requirements:
1. Title should be a positional ARGUMENT, not an option with prompt
2. Description should be --description option (optional, no prompt)
3. Task ID should be a positional ARGUMENT for view/update/delete/complete/uncomplete

Expected usage:
- todo add "Buy groceries"
- todo add "Buy groceries" --description "Milk, eggs, bread"
- todo list
- todo list --status pending
- todo view 1
- todo update 1 --title "New title"
- todo update 1 --description "New description"
- todo complete 1
- todo uncomplete 1
- todo delete 1

Reference Task: T-008 from specs/todo-console-app/tasks.md
Follow the CLI Commands Specification from specs/todo-console-app/spec.md

## Response snapshot

Fixed the CLI commands in src/hackathon_todo/cli/commands.py to meet the requirements:

1. Changed the add command to accept title as a positional argument instead of --title option
2. Added --description option to add command
3. Added --status option to list command to filter by status
4. Confirmed that task ID is already a positional argument for view/update/delete/complete/uncomplete commands
5. Updated the list command handler to support filtering by status

The changes made:
- Modified the add command decorator to use @click.argument('title', type=str) instead of @click.option('--title', ...)
- Added @click.option('--description', default='', help='Description of the task') to the add command
- Added @click.option('--status', type=click.Choice(['pending', 'completed']), help='Filter tasks by status') to the list command
- Updated the list command handler to filter tasks by status when provided
- Verified that all other commands (view, update, delete, complete, uncomplete) already use task_id as a positional argument

The CLI now supports the expected usage patterns:
- todo add "Buy groceries"
- todo add "Buy groceries" --description "Milk, eggs, bread"
- todo list
- todo list --status pending
- todo view 1
- todo update 1 --title "New title"
- todo update 1 --description "New description"
- todo complete 1
- todo uncomplete 1
- todo delete 1

## Outcome

- ✅ Impact: Fixed CLI command structure to match requirements
- 🧪 Tests: Manual verification performed
- 📁 Files: Modified commands.py to update CLI structure
- 🔁 Next prompts: N/A
- 🧠 Reflection: Successfully updated the CLI to meet the specified requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A