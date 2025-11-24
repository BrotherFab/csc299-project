const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const { readTasks, writeTasks, TASKS_FILE } = require('../src/storage');

const TEST_DATA_DIR = path.dirname(TASKS_FILE);
const BACKUP_FILE = TASKS_FILE + '.backup';

describe('Storage', () => {
  beforeEach(() => {
    // Always start from a clean slate
    if (fs.existsSync(TASKS_FILE)) {
      fs.unlinkSync(TASKS_FILE);
    }
    if (fs.existsSync(BACKUP_FILE)) {
      fs.unlinkSync(BACKUP_FILE);
    }
    if (fs.existsSync(TEST_DATA_DIR)) {
      fs.rmSync(TEST_DATA_DIR, { recursive: true, force: true });
    }
  });

  afterEach(() => {
    // And clean up after each test too
    if (fs.existsSync(TASKS_FILE)) {
      fs.unlinkSync(TASKS_FILE);
    }
    if (fs.existsSync(BACKUP_FILE)) {
      fs.unlinkSync(BACKUP_FILE);
    }
    if (fs.existsSync(TEST_DATA_DIR)) {
      fs.rmSync(TEST_DATA_DIR, { recursive: true, force: true });
    }
  });

  describe('readTasks', () => {
    it('should return empty tasks array when file does not exist', () => {
      const data = readTasks();
      assert.deepStrictEqual(data, { tasks: [] });
    });

    it('should read existing tasks from file', () => {
      const testData = {
        tasks: [
          { id: 1, description: 'Test task', created: '2025-11-24T10:00:00Z' }
        ]
      };
      fs.mkdirSync(TEST_DATA_DIR, { recursive: true });
      fs.writeFileSync(TASKS_FILE, JSON.stringify(testData), 'utf8');

      const data = readTasks();
      assert.deepStrictEqual(data, testData);
    });

    it('should throw error on malformed JSON', () => {
      fs.mkdirSync(TEST_DATA_DIR, { recursive: true });
      fs.writeFileSync(TASKS_FILE, 'invalid json', 'utf8');

      assert.throws(() => readTasks(), /Failed to read tasks/);
    });

    it('should create data directory if it does not exist', () => {
      if (fs.existsSync(TEST_DATA_DIR)) {
        fs.rmSync(TEST_DATA_DIR, { recursive: true });
      }
      
      const data = readTasks();
      assert.ok(fs.existsSync(TEST_DATA_DIR));
      assert.deepStrictEqual(data, { tasks: [] });
    });
  });

  describe('writeTasks', () => {
    it('should write tasks to file', () => {
      const testData = {
        tasks: [
          { id: 1, description: 'Test task', created: '2025-11-24T10:00:00Z' }
        ]
      };

      writeTasks(testData);

      assert.ok(fs.existsSync(TASKS_FILE));
      const content = fs.readFileSync(TASKS_FILE, 'utf8');
      assert.deepStrictEqual(JSON.parse(content), testData);
    });

    it('should create data directory if it does not exist', () => {
      if (fs.existsSync(TEST_DATA_DIR)) {
        fs.rmSync(TEST_DATA_DIR, { recursive: true });
      }

      const testData = { tasks: [] };
      writeTasks(testData);

      assert.ok(fs.existsSync(TEST_DATA_DIR));
      assert.ok(fs.existsSync(TASKS_FILE));
    });

    it('should format JSON with proper indentation', () => {
      const testData = {
        tasks: [{ id: 1, description: 'Test', created: '2025-11-24T10:00:00Z' }]
      };

      writeTasks(testData);

      const content = fs.readFileSync(TASKS_FILE, 'utf8');
      // Check that it's properly formatted (has newlines and spaces)
      assert.ok(content.includes('\n'));
      assert.ok(content.includes('  '));
    });
  });
});
