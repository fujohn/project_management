from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import project, user
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
        self.user_id = data["user_id"]
        self.project = None
        self.assigner = None
        self.assignee = None

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
    def get_all_non_user_tasks(cls):
        query="""
        SELECT * FROM tasks 
        JOIN projects on projects.id = tasks.project_id
        WHERE tasks.assignee_id != projects.user_id;
        """
        results=connectToMySQL(cls.db_name).query_db(query)
        tasks=[]
        for row in results:
            task=cls(row)
            task_creator_info={
                "id":row["assigner_id"],
                "name":row["name"]
            }
            creator= user.User(task_creator_info)
            task.creator=creator
            tasks.append(task)
        return tasks
    
    @classmethod
    def get_all_user_tasks(cls):
        query="""
        SELECT * FROM tasks 
        JOIN users on tasks.assignee_id = users.id
        JOIN projects on projects.id = tasks.project_id;
        """
        results=connectToMySQL(cls.db_name).query_db(query)
        tasks=[]
        for row in results:
            task=cls(row)
            task_creator_info={
                "id":row["assigner_id"],
                "name":row["name"]
            }
            creator= user.User(task_creator_info)
            task.creator=creator
            tasks.append(task)
        return tasks
    
    @classmethod
    def get_task_by_id(cls, id):
        data={"id":id}
        query="""
        SELECT * FROM tasks WHERE id = %(id)s;
        """
        result =connectToMySQL(cls.db_name).query_db(query,data)
        if len(result) == 0:
            return False
        else:
            return cls(result[0])
        
# Update
    @classmethod
    def update_task(cls,data):
        query="""
        UPDATE tasks SET
        name = %(name)s,
        due_date = %(due_date)s,
        description = %(description)s,
        is_complete = %(is_complete)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query)
    
# Delete
    @classmethod
    def delete_task_by_id(cls,task_id):
        data={"id":task_id}
        query="""
        DELETE FROM tasks WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query,data)
    
# --------------------------Create Static Methods--------------------------------#
# Static methods are used for validation of the data that is input

    @staticmethod
    def validate_task(task):
        is_valid = True
        if len(task["name"]) < 3:
            flash("Name must be more than 3 characters long", "create_task")
            is_valid = False
        if len(task["due_date"]) < 0:
            flash("Must select a due date!", "create_task")
            is_valid = False
        if len(task["description"]) < 5:
            flash("Task description must be at least 5 characters long", "create_task")
            is_valid = False
        # if len(task["is_complete"]) < 5:
        #     flash("Task description must be at least 5 characters long", "create_task")
        #     is_valid = False
        return is_valid
