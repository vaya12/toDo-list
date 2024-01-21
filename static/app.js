
document.addEventListener('DOMContentLoaded', function () {
    const taskForm = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');
    const modal = document.getElementById('editModal');
    const editForm = document.getElementById('editForm');
    const editTitle = document.getElementById('editTitle');
    const editDescription = document.getElementById('editDescription');
    const editDone = document.getElementById('editDone');
    const closeModal = document.getElementById('closeModal');

    let editingTask = null;

    taskForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;

        const newTask = document.createElement('li');
        newTask.innerHTML = `<span class="taskTitle">${title}</span> - <span class="taskDescription">${description}</span>
                             <button class="editBtn">Edit</button>
                             <button class="deleteBtn">Delete</button>`;
        taskList.appendChild(newTask);

        taskForm.reset();
    });

    taskList.addEventListener('click', function (event) {
        if (event.target.classList.contains('deleteBtn')) {
            event.target.parentElement.remove();
        } else if (event.target.classList.contains('editBtn')) {
            editingTask = event.target.parentElement;
            const taskText = editingTask.querySelector('.taskTitle').textContent;
            const taskDescription = editingTask.querySelector('.taskDescription').textContent;
            const isDone = editingTask.classList.contains('done');

            editTitle.value = taskText;
            editDescription.value = taskDescription;
            editDone.checked = isDone;

            modal.style.display = 'block';
        } else if (event.target.classList.contains('taskTitle')) {
            const task = event.target.parentElement;
            task.classList.toggle('done');
        }
    });

    editForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const editedTitle = editTitle.value;
        const editedDescription = editDescription.value;

        editingTask.querySelector('.taskTitle').textContent = editedTitle;
        editingTask.querySelector('.taskDescription').textContent = editedDescription;

        if (editDone.checked) {
            editingTask.classList.add('done');
        } else {
            editingTask.classList.remove('done');
        }

        modal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });
});
