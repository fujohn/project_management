from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)

class User:
    db_name = "proj_mgm_group_project"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.projects = []
        self.tasks = []
        self.assigned_tasks = []

# Create
    @classmethod
    def create_user(cls, data):

        # change made here to validate registration before user creation
        if not cls.validate_registration(data):
            return False
        
        # changes made here to hash password
        pw_hash = bcrypt.generate_password_hash(data['password'])
        user = data.copy()
        user["password"] = pw_hash
        query = '''
        INSERT INTO users
        (name, email, password)
        VALUES (%(name)s, %(email)s, %(password)s)
        ;'''
        return connectToMySQL(cls.db_name).query_db(query, user)

# Read
    @classmethod
    def get_user_by_id(cls, data):
        query = '''
        SELECT * FROM users
        WHERE id = %(id)s
        ;'''
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results:
            return None
        else:
            return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = '''
        SELECT * FROM users
        WHERE email = %(email)s
        ;'''
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else: 
            return results[0]

# Validations

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Name must be at least 3 characters!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!', 'register')
            is_valid = False
        user_email = {
            'email': data['email']
        }
        is_email_taken = User.get_user_by_email(user_email)
        if is_email_taken != None:
            flash('Email address already registered!', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters!', 'register')
            is_valid = False
        if data['confirm_pw'] != data['password']:
            flash("Passwords don't agree!", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid login credentials!", 'login')
            return False
        user_email = {
            'email': data['email']
        }
        is_email_taken = User.get_user_by_email(user_email)
        if is_email_taken == None:
            flash("Email not registered!", 'login')
            return False
        if not bcrypt.check_password_hash(is_email_taken['password'], data['password']):
            flash("Invalid login credentials!", 'login')
            return False
        return is_email_taken
    
