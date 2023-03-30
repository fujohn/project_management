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
        LEFT JOIN users 
        ON projects.user_id = users.id
        WHERE projects.id = %(project_id)s
        ;'''
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if not result:
            return None
        else:
            print(result)
            this_proj = cls(result[0])
            this_user_dict = {
                'id': result[0]['users.id'],
                'name': result[0]['users.name'],
                'email': result[0]['email'],
                'password': result[0]['password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at']
            }
            this_user_obj = user.User(this_user_dict)
            this_proj.assigner = this_user_obj
            for one_task in result:
                task_dict = {
                    'id': one_task['tasks.id'],
                    'name': one_task['name'],
                    'due_date': one_task['due_date'],
                    'description': one_task['tasks.description'],
                    'is_complete': one_task['is_complete'],
                    'created_at': one_task['tasks.created_at'],
                    'updated_at': one_task['tasks.updated_at']
                }
                this_task_assigner = user.User.get_user_by_id(one_task['assigner_id'])
                this_task_assignee = user.User.get_user_by_id(one_task['assignee_id'])
                this_task_obj = task.Task(task_dict)
                this_task_obj.assignee = this_task_assignee
                this_task_obj.assigner = this_task_assigner
                this_task_obj.project = this_proj
                this_proj.tasks.append(this_task_obj)
            return this_proj

    # check validation code here
    @staticmethod
    def validate_project(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Project title must be at least 3 characters long.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Project description must be at least 3 characters long.")
            is_valid = False
        return is_valid

    # delete project here
    @classmethod
    def delete_project_by_id(cls, project_id):
        data={"id" : project_id}
        query ="""
        DELETE FROM projects
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result

    # edit
    @classmethod
    def update_project(cls, project_dict):
        project = cls.get_one_project_by_id(project_dict["id"])
        query = '''
        UPDATE projects
        SET title = %(title)s, description = %(description)s
        WHERE id = %(id)s
        ;'''
        result = connectToMySQL(cls.db_name).query_db(query, project_dict)
        return result
