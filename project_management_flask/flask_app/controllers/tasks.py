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
    data = {
        'id': task_id
    }
    task=Task.get_task_by_id(data)
    return render_template(task_detail_page, task=task)

# Create a task GET route
@app.route("/tasks/new")
def new_task():
    if "user_id" not in session:
        return redirect("/")
    all_projects = Project.get_all_projects()
    all_users = User.get_all_users()
    # some get all user method here
    return render_template(new_task_page, all_projects=all_projects, all_users=all_users)

# Edit a task GET route
@app.route("/tasks/<int:task_id>/edit")
def edit_task(task_id):
    if "user_id" not in session:
        return redirect("/")
    data= {
        'id': task_id
    }
    all_users = User.get_all_users()
    task=Task.get_task_by_id(data)
    project=Task.get_user_tasks_by_project(data)
    return render_template(edit_task_page, task=task, all_users=all_users, project=project)

# Create a task POST route
@app.route("/create_task", methods=["POST"])
def create_new_task():
    if "user_id" not in session:
        return redirect('/')
    if not Task.validate_task(request.form):
        return redirect("/tasks/new")
    Task.create_task(request.form)
    return redirect(f"/projects/{request.form['project_id']}")

# Update a task POST route
@app.route("/tasks/<int:task_id>/update", methods=["POST"])
def update_task(task_id):
    if "user_id" not in session:
        return redirect("/")
    if not Task.validate_task(request.form):
        return redirect(f"/tasks/{task_id}/edit")
    print('------------------------------------------------------------ Running update query ---------------------------------------')
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
    if 'project_id' in session:
        return redirect(f"/projects/{session['project_id']}")
    else:
        return redirect(user_dashboard)

# Delete a task route
@app.route("/tasks/<int:id>/delete")
def delete_task(id):
    if "user_id" not in session:
        return redirect("/")
    Task.delete_task_by_id(id)
    return redirect("/dashboard")
