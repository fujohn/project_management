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

# Single Task Details Page
@app.route("/tasks/<int:task_id>")
def task_detail(task_id):
    if "user_id" not in session:
        redirect("/")
    user= User.get_user_by_id(session["user_id"])
    task=Task.get_task_by_id(task_id)
    return render_template(task_detail_page, user=user, task=task)

# Create a task POST route
@app.route("/create_task", methods=["POST"])
def create_new_task():
    if "user_id" not in session:
        redirect('/')
    if Task.validate_task(request.form):
        Task.create_task(request.form)
    user = User.get_user_by_id(session["user_id"])
    return render_template(new_task_page, user=user)

# Create a task GET route
@app.route("/tasks/new")
def new_task():
    if "user_id" not in session:
        redirect("/")
    user = User.get_user_by_id(session["user_id"])
    return render_template(new_task_page, user=user)

# Update a task POST route
@app.route("/tasks/<int:task_id>/edit")
def update_task(task_id):
    if "user_id" not in session:
        redirect("/")
    if Task.validate_task(request.form):
        Task.update_task(request.form)
        return redirect(projects_page)
    return redirect(f"/tasks/{task_id}/edit")

# Delete a task route
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect("/")
    Task.delete_task_by_id(task_id)
    return redirect(projects_page)
