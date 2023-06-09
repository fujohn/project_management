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
        self.project = None
        self.assigner = None
        self.assignee = None

# Create
    @classmethod
    def create_task(cls, data):
        query = '''
        INSERT INTO tasks 
        (name, due_date, description, is_complete, project_id, assigner_id, assignee_id)
        VALUES (%(name)s, %(due_date)s, %(description)s, 0, %(project_id)s, %(assigner_id)s, %(assignee_id)s)
        ;'''
        return connectToMySQL(cls.db_name).query_db(query, data)

# Read 
    @classmethod
    def get_other_tasks_by_project(cls, data):
        query="""
        SELECT * FROM tasks 
        JOIN projects on projects.id = tasks.project_id
        WHERE tasks.assignee_id != %(user_id)s
        AND projects.id = %(project_id)s
        AND is_complete = 0
        ORDER BY due_date;
        """
        results=connectToMySQL(cls.db_name).query_db(query,data)
        # print(results)
        tasks=[]
        for row in results:
            task=cls(row)
            task_creator_info={
                "id":row["assigner_id"],
                "name":row["name"]
            }
            task_assignee_info={
                "id":row["assignee_id"],
                "name":row["name"]
            }
            creator= user.User.get_user_by_id(task_creator_info)
            task.assigner=creator
            assignee= user.User.get_user_by_id(task_assignee_info)
            task.assignee=assignee
            tasks.append(task)
        return tasks
    
    @classmethod
    def get_user_tasks_by_project(cls, data):
        query="""
        SELECT * FROM tasks 
        JOIN projects on projects.id = tasks.project_id
        WHERE tasks.assignee_id = %(user_id)s
        AND projects.id = %(project_id)s
        AND is_complete = 0
        ORDER BY due_date;
        """
        results=connectToMySQL(cls.db_name).query_db(query,data)
        # print(results)
        tasks=[]
        for row in results:
            task=cls(row)
            task_creator_info={
                "id":row["assigner_id"],
                "name":row["name"]
            }
            task_assignee_info={
                "id":row["assignee_id"],
                "name":row["name"]
            }
            creator= user.User.get_user_by_id(task_creator_info)
            task.assigner=creator
            assignee= user.User.get_user_by_id(task_assignee_info)
            task.assignee=assignee
            tasks.append(task)
        return tasks
    
    @classmethod
    def get_completed_tasks_by_project(cls, data):
        query="""
        SELECT * FROM tasks 
        JOIN projects on projects.id = tasks.project_id
        WHERE projects.id = %(project_id)s
        AND is_complete = 1
        ORDER BY due_date;
        """
        results=connectToMySQL(cls.db_name).query_db(query,data)
        tasks=[]
        for row in results:
            task=cls(row)
            task_creator_info={
                "id":row["assigner_id"],
                "name":row["name"]
            }
            task_assignee_info={
                "id":row["assignee_id"],
                "name":row["name"]
            }
            creator= user.User.get_user_by_id(task_creator_info)
            task.assigner=creator
            assignee= user.User.get_user_by_id(task_assignee_info)
            task.assignee=assignee
            tasks.append(task)
        return tasks
    
    @classmethod
    def get_active_user_tasks(cls, data):
        query="""
        SELECT * FROM tasks 
        JOIN users on tasks.assignee_id = users.id
        JOIN projects on projects.id = tasks.project_id
        WHERE users.id = %(id)s
        AND is_complete = 0
        ORDER BY due_date;
        """
        results=connectToMySQL(cls.db_name).query_db(query,data)
        tasks=[]
        for row in results:
            task=cls(row)
            project_info={
                "project_id":row["project_id"]
            }
            task_creator_info={
                "id":row["assigner_id"],
                "name":row["name"]
            }
            task_assignee_info={
                "id":row["assignee_id"],
                "name":row["name"]
            }
            for_project = project.Project.get_one_project_by_id(project_info)
            task.project = for_project
            creator= user.User.get_user_by_id(task_creator_info)
            task.assigner=creator
            assignee= user.User.get_user_by_id(task_assignee_info)
            task.assignee=assignee
            tasks.append(task)
        return tasks
    
    @classmethod
    def get_task_by_id(cls, data):
        query="""
        SELECT * 
        FROM tasks 
        WHERE id = %(id)s
        ORDER BY due_date;
        """
        result =connectToMySQL(cls.db_name).query_db(query,data)
        if not result:
            return False
        else:
            task=cls(result[0])
            project_info={
                "project_id":result[0]["project_id"]
            }
            task_creator_info={
                "id":result[0]["assigner_id"],
                "name":result[0]["name"]
            }
            task_assignee_info={
                "id":result[0]["assignee_id"],
                "name":result[0]["name"]
            }
            for_project = project.Project.get_one_project_by_id(project_info)
            task.project = for_project
            creator= user.User.get_user_by_id(task_creator_info)
            task.assigner=creator
            assignee= user.User.get_user_by_id(task_assignee_info)
            task.assignee=assignee
            return task
        
# Update
    @classmethod
    def update_task(cls,data):
        query="""
        UPDATE tasks SET
        name = %(name)s,
        due_date = %(due_date)s,
        description = %(description)s,
        assignee_id = %(assignee_id)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def complete_task(cls,data):
        query="""
        UPDATE tasks SET
        is_complete = 1
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query,data)
    
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
        if len(task['project_id']) < 1:
            flash("Please select an affiliated project", "create_task")
            is_valid = False
        if len(task["name"]) < 3:
            flash("Name must be more than 3 characters long", "create_task")
            is_valid = False
        if len(task["due_date"]) < 1:
            flash("Must select a due date!", "create_task")
            is_valid = False
        if len(task["description"]) < 5:
            flash("Task description must be at least 5 characters long", "create_task")
            is_valid = False
        return is_valid
