document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-add-task');
    const addTaskForm  = document.getElementById('add-task-form');
    const taskList     = document.getElementById('task-list');

    // Toggle Add Task form
    if (toggleButton && addTaskForm) {
        toggleButton.addEventListener('click', (e) => {
            e.stopPropagation();
            addTaskForm.classList.toggle('visible'); // toggle visibility
        });
    }

    // Toggle per-task edit/delete form
    if (taskList) {
        taskList.addEventListener('click', (event) => {
            const taskText = event.target.closest('.task-text');
            if (!taskText) return;

            const li = taskText.closest('li');
            if (!li) return;

            const form = li.querySelector('.task-form');
            if (form) {
                form.classList.toggle('visible');
            }
        });
    }
});
