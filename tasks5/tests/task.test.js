const { describe, it, beforeEach } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

const { addTask, listTasks } = require('../src/task');
const { TASKS_FILE } = require('../src/storage');

const DATA_DIR = path.dirname(TASKS_FILE);

describe('Task', { concurrency: false }, () => {
  // Make sure every test starts with a clean data directory & file
  beforeEach(() => {
    if (fs.existsSync(DATA_DIR)) {
      fs.rmSync(DATA_DIR, { recursive: true, force: true });
    }
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(TASKS_FILE, JSON.stringify({ tasks: [] }, null, 2), 'utf8');
  });

  describe('addTask', () => {
    it('should add a task with auto-incremented ID', () => {
      const task = addTask('First task');
      assert.strictEqual(task.id, 1);
      assert.strictEqual(task.description, 'First task');
    });

    it('should increment ID for multiple tasks', () => {
      const t1 = addTask('First');
      const t2 = addTask('Second');
      assert.strictEqual(t1.id, 1);
      assert.strictEqual(t2.id, 2);
    });

    it('should trim whitespace from description', () => {
      const task = addTask('   spaced out   ');
      assert.strictEqual(task.description, 'spaced out');
    });

    it('should throw error for empty description', () => {
      assert.throws(() => addTask(''), Error);
    });

    it('should throw error for whitespace-only description', () => {
      assert.throws(() => addTask('   '), Error);
    });

    it('should throw error for null description', () => {
      assert.throws(() => addTask(null), Error);
    });

    it('should throw error for undefined description', () => {
      assert.throws(() => addTask(undefined), Error);
    });

    it('should persist task to file', () => {
      const created = addTask('Persist me');
      const raw = fs.readFileSync(TASKS_FILE, 'utf8');
      const data = JSON.parse(raw);

      assert.ok(Array.isArray(data.tasks));
      const stored = data.tasks.find(t => t.id === created.id);
      assert.ok(stored);
      assert.strictEqual(stored.description, 'Persist me');
    });
  });

  describe('listTasks', () => {
    it('should return empty array when no tasks exist', () => {
      const tasks = listTasks();
      assert.deepStrictEqual(tasks, []);
    });

    it('should return all tasks', () => {
      addTask('Task 1');
      addTask('Task 2');

      const tasks = listTasks();
      assert.strictEqual(tasks.length, 2);
      const descriptions = tasks.map(t => t.description);
      assert.deepStrictEqual(descriptions, ['Task 1', 'Task 2']);
    });

    it('should return tasks in order they were added', () => {
      addTask('First');
      addTask('Second');
      addTask('Third');

      const tasks = listTasks();
      const descriptions = tasks.map(t => t.description);
      assert.deepStrictEqual(descriptions, ['First', 'Second', 'Third']);
    });
  });
});
