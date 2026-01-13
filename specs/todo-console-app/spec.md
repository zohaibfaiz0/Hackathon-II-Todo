# Specification: Phase I Console Todo App

## 1. Overview

### 1.1 Purpose
Build a Python console application for managing personal todo tasks. This application serves as Phase I of "The Evolution of Todo" project, implementing the 5 Basic Level features as specified in the project constitution.

### 1.2 Scope
- **In Scope**: Console-based task management with add, view, update, delete, and complete/incomplete functionality
- **Out of Scope**: Web interface, user authentication, cloud synchronization, advanced filtering

### 1.3 Success Criteria
- All 5 Basic Level features implemented per constitution
- 100% type coverage in Python code
- Zero runtime errors on first deployment
- Adherence to layered architecture (PRESENTATION → APPLICATION → DOMAIN → INFRASTRUCTURE)

---

## 2. Functional Requirements

### 2.1 US-001: Add Task
**Feature**: Create new tasks with title and optional description

#### Acceptance Criteria:
- System accepts title (required, 1-200 characters) and description (optional, max 1000 characters)
- System generates unique ID and timestamps automatically
- Task is stored in local storage (JSON file)
- Confirmation message displayed upon successful creation
- Proper validation and error messages for invalid inputs

#### Edge Cases:
- Empty or whitespace-only title rejected
- Title exceeding 200 characters rejected
- Description exceeding 1000 characters rejected

### 2.2 US-002: View Task List
**Feature**: Display all tasks in a formatted table

#### Acceptance Criteria:
- Displays ID, title, status, and creation date
- Status shown as ⬜ Pending or ✅ Done
- Formatted table presentation with clear columns
- Message shown when no tasks exist

### 2.3 US-003: Update Task
**Feature**: Modify existing task's title or description by ID

#### Acceptance Criteria:
- System accepts task ID and new values for title and/or description
- Updates the `updated_at` timestamp
- Validates new values per creation rules
- Confirmation message displayed upon successful update
- Error message when task ID doesn't exist

### 2.4 US-004: Delete Task
**Feature**: Remove task by ID

#### Acceptance Criteria:
- System accepts task ID for deletion
- Task permanently removed from storage
- Confirmation message displayed
- Error message when task ID doesn't exist

### 2.5 US-005: Mark Complete/Incomplete
**Feature**: Toggle task completion status

#### Acceptance Criteria:
- Separate commands for marking complete and incomplete
- Updates task's completion status
- Updates the `updated_at` timestamp
- Confirmation message displayed
- Error message when task ID doesn't exist

---

## 3. Technical Architecture

### 3.1 Layered Architecture Implementation

#### Presentation Layer:
- Command-line interface using `argparse` or similar
- Console input/output handling
- User interaction flow management

#### Application Layer:
- Service functions coordinating operations
- Business logic orchestration
- Input validation and error handling

#### Domain Layer:
- Task entity definition with validation rules
- Business rule enforcement
- Core data structures and methods

#### Infrastructure Layer:
- Local file storage (JSON)
- Persistence mechanisms
- Data access operations

### 3.2 Technology Stack
- **Runtime**: Python 3.13+
- **Package Manager**: UV
- **Type Checking**: mypy (strict)
- **Linting/Format**: ruff
- **Storage**: Local JSON file

---

## 4. Data Model

### 4.1 Task Entity
```python
class Task:
    id: str (UUID)
    title: str (1-200 characters)
    description: str (optional, max 1000 characters)
    completed: bool (default False)
    created_at: datetime (auto-generated)
    updated_at: datetime (auto-generated)
```

### 4.2 Validation Rules
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Completed: Boolean, defaults to False
- Timestamps: Auto-generated, never user-provided

---

## 5. User Interface

### 5.1 Command Structure
```
todo-cli [command] [arguments]

Commands:
- add --title "Title" [--description "Description"]
- list
- update --id ID [--title "New Title"] [--description "New Description"]
- delete --id ID
- complete --id ID
- uncomplete --id ID
```

### 5.2 Expected Output Formats
- **Add Task**: "Task 'X' created successfully with ID: Y"
- **List Tasks**: Formatted table with ID, Title, Status, Created Date
- **Update Task**: "Task 'X' updated successfully"
- **Delete Task**: "Task 'X' deleted successfully"
- **Complete Task**: "Task 'X' marked as complete"
- **Uncomplete Task**: "Task 'X' marked as incomplete"

---

## 6. Error Handling

### 6.1 Error Categories
- **Validation Errors**: Invalid input data
- **Not Found Errors**: Task ID doesn't exist
- **System Errors**: File I/O or storage issues

### 6.2 Error Messages
- User-friendly messages for all error conditions
- Specific error codes for debugging
- No stack traces in production mode

---

## 7. Security Considerations

### 7.1 Data Protection
- No sensitive data stored
- Local storage only
- Input sanitization at all boundaries

---

## 8. Quality Requirements

### 8.1 Testing Requirements
- Domain/Models: 100% coverage
- Services: 90% coverage
- CLI Commands: 85% coverage
- Test naming: `test_<action>_<condition>_<result>`

### 8.2 Documentation Requirements
- README.md with setup instructions
- Docstrings on all public interfaces
- CLI help text for all commands

---

## 9. Constraints

### 9.1 Performance
- Sub-second response times for all operations
- Efficient JSON parsing and writing

### 9.2 Size Limitations
- Maximum 200 lines per file
- Maximum 50 lines per function

---

## 10. Future Considerations

### 10.1 Phase Transition Preparation
- Domain layer designed for portability to Phase II
- Abstraction layers to support future infrastructure changes
- API contracts designed to support web interface in Phase II

---

**Version**: 1.0.0
**Created**: 2026-01-13
**Approved**: Pending
