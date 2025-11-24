#!/usr/bin/env node

const { addTask, listTasks } = require('./task');
const packageJson = require('../package.json');

function showHelp() {
  console.log(`
Task Manager CLI v${packageJson.version}

Usage:
  task add <description>    Add a new task
  task list                 List all tasks
  task --help              Show this help message
  task --version           Show version number

Examples:
  task add "Buy groceries"
  task list
  `);
}

function showVersion() {
  console.log(packageJson.version);
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    showHelp();
    return;
  }

  if (args[0] === '--version') {
    showVersion();
    return;
  }

  const command = args[0];

  try {
    switch (command) {
      case 'add': {
        const description = args.slice(1).join(' ');
        if (!description) {
          console.error('Error: Task description is required');
          console.log('Usage: task add <description>');
          process.exit(1);
        }
        const task = addTask(description);
        console.log(`✓ Task added: #${task.id} - ${task.description}`);
        break;
      }

      case 'list': {
        const tasks = listTasks();
        if (tasks.length === 0) {
          console.log('No tasks found');
        } else {
          console.log(`\nTasks (${tasks.length}):\n`);
          tasks.forEach(task => {
            console.log(`  #${task.id} - ${task.description}`);
          });
          console.log();
        }
        break;
      }

      default:
        console.error(`Error: Unknown command '${command}'`);
        console.log('Run "task --help" for usage information');
        process.exit(1);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };
