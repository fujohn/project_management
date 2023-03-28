from flask import Flask, render_template, session, redirect, request, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.task import Task
from flask_app.models.project import Project

registration_page = 'login.html'
projects_page = 'projects.html'
user_dashboard = '/dashboard'
task_detail_page = 'task_details.html'
new_task_page = 'new_tasks.html'
edit_task_page = 'edit_task.html'

# Single Task Details Page
@app.route("/tasks/<int:task_id>")
def task_detail(task_id):
    if "user_id" not in session:
        return redirect("/")
    user= User.get_user_by_id(session["user_id"])
    task=Task.get_task_by_id(task_id)
    return render_template(task_detail_page, user=user, task=task)

# Create a task GET route
@app.route("/tasks/new")
def new_task():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id(session["user_id"])
    return render_template(new_task_page, user=user)

# Edit a task GET route
@app.route("/tasks/<int:task_id>/edit")
def edit_task(task_id):
    if "user_id" not in session:
        return redirect("/")
    user = User.get_user_by_id(session["user_id"])
    task=Task.get_task_by_id(task_id)
    return render_template(edit_task_page, user=user, task=task)

# Create a task POST route
@app.route("/create_task", methods=["POST"])
def create_new_task():
    if "user_id" not in session:
        return redirect('/')
    if not Task.validate_task(request.form):
        return redirect("/tasks/new")
    task = Task.create_task(request.form)
    return redirect(f"/project/{task.project.id}")

# Update a task POST route
@app.route("/tasks/<int:task_id>/update", methods=["POST"])
def update_task(task_id):
    if "user_id" not in session:
        return redirect("/")
    if not Task.validate_task(request.form):
        return redirect(f"/tasks/{task_id}/edit")
    Task.update_task(request.form)
    return redirect(f"/tasks/{task_id}")

# complete a task POST route
@app.route("/tasks/<int:task_id>/complete")
def complete_task(task_id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        'id': task_id
    }
    Task.complete_task(data)
    return redirect(user_dashboard)

# Delete a task route
@app.route("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task_to_delete = Task.get_task_by_id(task_id)
    if "user_id" not in session:
        return redirect("/")
    Task.delete_task_by_id(task_id)
    return redirect(f"/project/{task_to_delete.project.id}")
