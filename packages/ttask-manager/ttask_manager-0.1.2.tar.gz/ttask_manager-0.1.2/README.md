# TaskManager

TaskManager is a simple Python package for managing tasks. It's designed to be used in command-line interface (CLI) applications, providing basic task management functionality.

## Description

This package was created as part of a learning project to understand Python package development and distribution. While it's not intended to be a comprehensive task management solution, it serves as a practical example of how to structure and package a Python project.

The TaskManager package provides functionality to:
- Add tasks to a to-do list
- Mark tasks as completed
- Remove tasks from the list
- View current tasks and completed tasks

## What's new with the 0.1.1:

This release introduces a new feature that allows the TaskManager to save and load its state to/from a JSON file. This means that users can now persist their task lists across sessions, making it easier to manage their tasks. Additionally, the code has been refactored to improve readability and maintainability.

## Usage

Here's a quick example of how to use the TaskManager:

```python
from ttask_manager.ttask_manager import TaskManager

# Create a new TaskManager instance
tm = TaskManager()

# Add some tasks
tm.add_task("Write README", "Create setup.py", "Push to GitHub")

# View current tasks
print(tm.current_state('to-do'))

# Mark a task as done
tm.task_done("Write README")

# View completed tasks
print(tm.current_state('done'))
```

## Features

- Add multiple tasks at once
- Remove tasks from the to-do list
- Mark tasks as completed
- View current to-do list and completed tasks
- Clear to-do or completed lists
- Reset both lists

## Development
This project was primarily created as a learning exercise in Python package development. Its simplicity is intentional, and there are no plans for significant feature additions or expansions. However, if you find a bug or have a suggestion for a minor improvement, feel free to open an issue on the GitHub repository.

## Licensing

The code in this project is licensed under MIT license.

## Author

Taha Yasser Adnan

This project is part of my journey in learning Python package development. While it may not be a groundbreaking package, it represents an important step in understanding the process of creating, packaging, and distributing Python projects.

