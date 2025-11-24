const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const TASKS_FILE = path.join(DATA_DIR, 'tasks.json');

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

function readTasks() {
  try {
    ensureDataDir();

    if (!fs.existsSync(TASKS_FILE)) {
      return { tasks: [] };
    }

    const raw = fs.readFileSync(TASKS_FILE, 'utf8');

    if (!raw.trim()) {
      // empty file = empty tasks
      return { tasks: [] };
    }

    const data = JSON.parse(raw);

    // must have shape { tasks: [...] }
    if (!data || !Array.isArray(data.tasks)) {
      throw new Error('Invalid tasks format');
    }

    return data;

  } catch (err) {
    // the test expects regex: /Failed to read tasks/
    throw new Error(`Failed to read tasks: ${err.message}`);
  }
}

function writeTasks(data) {
  try {
    ensureDataDir();

    fs.writeFileSync(
      TASKS_FILE,
      JSON.stringify(data, null, 2), // prettified JSON for indentation test
      'utf8'
    );

  } catch (err) {
    throw new Error(`Failed to write tasks: ${err.message}`);
  }
}

module.exports = {
  TASKS_FILE,
  readTasks,
  writeTasks,
};
