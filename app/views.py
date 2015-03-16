from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from .forms import TaskForm
from .models import Task
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def list():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(raw = form.task.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('list'))
    tasks = Task.active_tasks().all()
    return render_template('list.html',
        form = form,
        title = 'Todo List',
        tasks = tasks)

# @app.route('/')
@app.route('/pomodoro')
def pomodoro():
    pick = Task.pick_one()
    if pick is None:
        flash("Cannot pick one task")
        return redirect(url_for('list'))
    return render_template('pomodoro.html',
        title = 'Pomodoro',
        pick = pick)

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        flash("Task not found")
        return redirect(url_for('pomorodo'))
    task.completed = True
    db.session.commit()
    return redirect(request.args.get('next') or url_for('pomodoro'))
