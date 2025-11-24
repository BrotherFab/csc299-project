const { readTasks, writeTasks } = require('./storage');

function addTask(description) {
  if (!description || description.trim().length === 0) {
    throw new Error('Task description cannot be empty');
  }

  const data = readTasks();
  const newId = data.tasks.length > 0 
    ? Math.max(...data.tasks.map(t => t.id)) + 1 
    : 1;

  const task = {
    id: newId,
    description: description.trim(),
    created: new Date().toISOString()
  };

  data.tasks.push(task);
  writeTasks(data);

  return task;
}

function listTasks() {
  const data = readTasks();
  return data.tasks;
}

module.exports = {
  addTask,
  listTasks
};
