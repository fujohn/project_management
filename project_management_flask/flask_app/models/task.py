from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import project
from flask import flash

class Task:
    db_name = "proj_mgm_group_project"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.due_date = data['due_date']
        self.description = data['description']
        self.is_complete = data['is_complete']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.project = None
        self.assigner = None
        self.assigee = None

# Create
    @classmethod
    def create_task(cls, data):
        query = '''
        INSERT INTO tasks 
        (name, due_date, description, is_complete, project_id, assigner_id, assignee_id)
        VALUES (%(name)s, %(due_date)s, %(description)s, %(is_complete)s, %(project_id)s, %(assigner_id)s, %(assignee_id)s)
        ;'''
        return connectToMySQL(cls.db_name).query_db(query, data)

# Read 
    @classmethod
    def get_all_tasks(cls, data):
        pass