from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User

# variablized route files
registration_page = 'index.html'
projects_page = 'projects.html'
user_dashboard = '/dashboard'


# registration page
@app.route('/')
def index():
    return render_template(registration_page)

# user registration route
@app.route("/register", methods=['POST'])
def register():
    valid_user = User.create_user(request.form)
    if not valid_user:
        return redirect('/')
    session["user_id"] = valid_user.id
    return redirect(user_dashboard)

@app.route("/login", methods=['POST'])
def login():
    valid_user = User.validate_login(request.form)
    if valid_user == False:
        return redirect('/')
    session["user_id"] = valid_user.id
    return redirect(user_dashboard)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')