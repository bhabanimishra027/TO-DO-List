document.addEventListener("DOMContentLoaded", function () {
  const taskList = document.getElementById("task-list");
  const addTaskBtn = document.getElementById("add-task-btn");
  const taskInput = document.getElementById("task-input");

  function createTaskElement(taskText) {
    const li = document.createElement("li");
    li.className = "task-item";

    // entry animation
    li.classList.add("fade-in");

    li.innerHTML = `
      <input type="checkbox" class="task-check">
      <span class="task-text">${taskText}</span>
      <button class="action-btn btn-edit">Edit</button>
      <button class="action-btn btn-delete">Delete</button>
    `;

    // mark complete
    // mark complete
    li.querySelector(".task-check").addEventListener("change", function () {
    if (this.checked) {
        li.classList.add("completed");
        this.classList.add("glow");
    } else {
        li.classList.remove("completed");
        this.classList.remove("glow");
    }
    });


    // edit task
    li.querySelector(".btn-edit").addEventListener("click", function () {
      const newText = prompt("Edit task:", li.querySelector(".task-text").textContent);
      if (newText) li.querySelector(".task-text").textContent = newText;
    });

    // delete task
    li.querySelector(".btn-delete").addEventListener("click", function () {
      li.classList.add("fade-out");
      setTimeout(() => li.remove(), 300);
    });

    return li;
  }

  addTaskBtn.addEventListener("click", function () {
    const taskText = taskInput.value.trim();
    if (taskText) {
      const newTask = createTaskElement(taskText);
      taskList.appendChild(newTask);
      taskInput.value = "";

      // small bounce animation after fade-in
      setTimeout(() => {
        newTask.classList.add("bounce");
      }, 300);
    }
  });
});
