from flask import Flask, render_template, session, redirect, request, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.task import Task
from flask_app.models.project import Project


# variablized route files

dashboard = 'projects.html'
project_detail_page = 'group_projects_dashboard.html'
new_project_page = 'projects_form_new.html'
edit_project = 'projects_form_edit.html'

@app.route('/dashboard')
def projects_home():
    if 'user_id' not in session:
        flash('You must be logged in to view this page!')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(data)
    projects = Project.get_all_projects()
    all_user_tasks = Task.get_active_user_tasks(data)

    return render_template(dashboard, user=user, projects = projects, tasks=all_user_tasks)


@app.route("/projects/<int:project_id>")
def project_detail(project_id):
    user_data = {'id': session['user_id']}
    
    data = {
        'project_id': project_id,
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    project = Project.get_one_project_by_id(data)
    own_tasks = Task.get_user_tasks_by_project(data)
    other_tasks = Task.get_other_tasks_by_project(data)
    completed_tasks = Task.get_completed_tasks_by_project(data)
    return render_template(project_detail_page, user=user, project=project, own_tasks=own_tasks, other_tasks=other_tasks, completed_tasks = completed_tasks)

@app.route("/new_project")
def new_project():
    data = {
        id: session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template(new_project_page, user=user)

@app.route("/create_project", methods=['POST'])
def create_new_project():
    print(session['user_id'])
    if not Project.validate_project(request.form):
        return redirect('/new_project')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': request.form['assigner']
    }
    new_project =Project.create_project(data)
    return redirect(f'/projects/{new_project}')

@app.route("/delete_project/<int:project_id>")
def delete_project(project_id):
    data = {
        'id': project_id
    }
    project = Project.get_one_project_by_id(data)
    if session['user_id'] != project.id:
        return redirect('/dashboard')
    data = {
        'id': project_id
    }
    Project.delete_project_by_id(data)
    return redirect('/dashboard')

@app.route("/edit_project/<int:project_id>")
def edit_project_page(project_id):
    project = Project.get_one_project_by_id(project_id)
    if session['user_id'] != project.id:
        return redirect('/dashboard')
    user = User.get_user_by_id(session['user_id'])
    return render_template(edit_project, user=user, project=project)

@app.route("/update_project/<int:project_id>", methods=['POST'])
def update_project(project_id):
    if not Project.validate_project(request.form):
        return redirect(f'/edit_project/{project_id}')
    data = {
        'id': project_id,
        'title': request.form['title'],
        'description': request.form['description']
    }
    Project.update_project(data)
    return redirect(f'/show/{project_id}')

