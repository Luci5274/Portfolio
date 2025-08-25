import os
import json
from flask import Flask, render_template, request, redirect, url_for
import secrets
import string

app = Flask(__name__)

# Fixed path to be absolute
DATA_FILE = os.path.join(app.root_path, 'todo.json')


def generate_unique_id(existing_ids, length=6):
    alphabet = string.ascii_letters + string.digits
    while True:
        new_id = ''.join(secrets.choice(alphabet) for _ in range(length))
        if new_id not in existing_ids:
            return new_id


def load_list():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, 'r') as f:
            todo = json.load(f)
    except json.JSONDecodeError:
        return []

    existing_ids = {task.get('id') for task in todo if task.get('id')}
    updated = False
    for task in todo:
        if 'id' not in task or not task['id']:
            task['id'] = generate_unique_id(existing_ids)
            existing_ids.add(task['id'])
            updated = True
    if updated:
        save_list(todo)

    return todo


def save_list(todo):
    with open(DATA_FILE, 'w') as f:
        json.dump(todo, f, indent=4)


@app.route('/add_task', methods=['POST'])
def add_task():
    todo = load_list()
    existing_ids = {task.get('id') for task in todo}
    new_task = {
        'id': generate_unique_id(existing_ids),
        'task': request.form['task'],
        'status': request.form['status'],
        'priority': request.form['priority']
    }
    todo.append(new_task)
    save_list(todo)
    return redirect(url_for('show_todo'))


@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
    todo = load_list()
    for task in todo:
        if task['id'] == task_id:
            task['task'] = request.form['task']
            task['status'] = request.form['status']
            task['priority'] = request.form['priority']
            break
    save_list(todo)
    return redirect(url_for('show_todo'))


@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    todo = load_list()
    todo = [task for task in todo if task['id'] != task_id]
    save_list(todo)
    return redirect(url_for('show_todo'))


@app.route('/')
def show_todo():
    todo_list = load_list()
    return render_template('index.html', todo=todo_list)


if __name__ == '__main__':
    app.run(debug=True)
