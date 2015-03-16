from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from .forms import TaskForm
from .models import Task
from datetime import datetime
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def list():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(raw = form.task.data, timestamp=datetime.utcnow(), completed = False)
        db.session.add(task)
        db.session.commit()
        flash("You added a new task")
        return redirect(url_for('list'))
    tasks = Task.active_tasks().all()
    return render_template('list.html',
        form = form,
        title = 'Todo List',
        tasks = tasks)

from random import choice

@app.route('/pomodoro')
def pomodoro():
    pick = choice(Task.pick_one().all())
    if pick is None:
        flash("There is no active task anymore")
        return redirect(url_for('list'))
    return render_template('pomodoro.html',
        title = 'Pomodoro',
        pick = pick)

@app.route('/compelete/<int:task_id>')
def complete(task_id):
    task = Task.query.get(task_id)
    task.compeleted = True
    db.session.commit()
    return redirect(url_for('pomodoro'))
