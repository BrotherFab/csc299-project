# Task Manager CLI

A simple command-line task manager with persistent JSON storage.

## Features

- Add tasks with descriptions
- List all tasks
- Persistent storage in JSON format
- Clean CLI interface with help and version commands
- Comprehensive unit tests

## Installation

```bash
npm install
```

## Usage

### Add a task
```bash
node src/cli.js add "Buy groceries"
node src/cli.js add "Write documentation"
```

### List all tasks
```bash
node src/cli.js list
```

### Show help
```bash
node src/cli.js --help
```

### Show version
```bash
node src/cli.js --version
```

## Testing

Run all unit tests:
```bash
npm test
```

## Project Structure

```
├── src/
│   ├── cli.js       # Command-line interface entry point
│   ├── storage.js   # File I/O operations
│   └── task.js      # Task operations (add, list)
├── tests/
│   ├── storage.test.js  # Storage module tests
│   └── task.test.js     # Task module tests
├── data/
│   └── tasks.json   # Task data (created automatically)
└── package.json
```

## Design Principles

This project follows these core principles:

- **Simplicity**: Straightforward code without unnecessary abstractions
- **Readability**: Self-documenting code with clear intent
- **Testability**: Modular, loosely coupled components with comprehensive tests
- **Clean CLI**: Standard conventions with clear error messages

## Data Format

Tasks are stored in `data/tasks.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "created": "2025-11-24T10:00:00.000Z"
    }
  ]
}
```

## Requirements

- Node.js >= 18.0.0 (uses native test runner)
