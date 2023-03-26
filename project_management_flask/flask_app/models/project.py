from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import task, user
from flask import flash

class Project:
    db_name = "proj_mgm_group_project"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.assigner = None
        self.tasks = []

# Create
    @classmethod
    def create_project(cls, data):
        query = '''
        INSERT INTO projects
        (title, description, user_id)
        VALUES (%(title)s, %(description)s, %(user_id)s)
        ;'''
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_projects(cls):
        query = '''
        SELECT * FROM projects
        LEFT JOIN users on users.id = projects.user_id
        ;'''
        results = connectToMySQL(cls.db_name).query_db(query)
        all_projects = []
        if len(results) == 0:
            return all_projects
        else:
            for one_proj in results:
                this_proj = cls(one_proj)
                this_user_dict = {
                    'id': one_proj['users.id'],
                    'name': one_proj['name'],
                    'email': one_proj['email'],
                    'password': one_proj['password'],
                    'created_at': one_proj['users.created_at'],
                    'updated_at': one_proj['users.updated_at']
                }
                this_user_obj = user.User(this_user_dict)
                this_proj.assigner = this_user_obj
                all_projects.append(this_proj)
            return all_projects

    @classmethod
    def get_one_project_by_id(cls, data):
        query = '''
        SELECT * FROM projects
        LEFT JOIN tasks
        ON tasks.project_id = projects.id
        WHERE projects.id = %(id)s
        ;'''
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            this_proj = cls(results[0])
        # In progress
