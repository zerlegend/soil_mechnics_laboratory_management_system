from smlms import mysql


# User Model
class User:
    def __init__(self, id, name, email, password, role, active, created_at, updated_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at


def get_user_by_email(email):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s ', (email, ))
            user_data = cursor.fetchone()
        return User(*user_data) if user_data else None
    except Exception as e:
        print(f"Error in get_user_by_email: {e}")
        return None

def create_user(name, email, password, role='user', active=True):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email, password, role, active) VALUES (%s, %s, %s, %s, %s)",
                           (name, email, password, role, active))
        mysql.connection.commit()
        return get_user_by_email(email)
    except Exception as e:
        print(f"Error in create_user: {e}")
        return None

def get_all_users():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users_data = cursor.fetchall()
        # Assuming User is a class representing your user model
        users = [User(*user_data) for user_data in users_data]
        return users
    except Exception as e:
        print(f"Error in get_all_users: {e}")
        return None


# Project Model
class Project:
    def __init__(self, id, name, location, description, start_date, end_date, budget, created_at, updated_at):
        self.id = id
        self.name = name
        self.location = location
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.created_at = created_at
        self.updated_at = updated_at


def get_all_projects():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM projects")
            project_data = cursor.fetchall()
        projects = [Project(*data) for data in project_data]
        return projects
    except Exception as e:
        print(f"Error in get_all_projects: {e}")
        return []

def get_project_by_id(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM projects WHERE id = %s", (id,))
            project_data = cursor.fetchone()
        return Project(*project_data) if project_data else None
    except Exception as e:
        print(f"Error in get_project_by_id: {e}")
        return None

def create_project(name, location, description, start_date, end_date, budget):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO projects (name, location, description, start_date, end_date, budget) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, location, description, start_date, end_date, budget))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in create_project: {e}")

def update_project_by_id(id, name, location, description, start_date, end_date, budget):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE projects SET name = %s, location = %s, description = %s, start_date = %s, end_date = %s, budget = %s WHERE id = %s",
                           (name, location, description, start_date, end_date, budget, id))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in update_project: {e}")

def delete_project_by_id(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM projects WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in delete_project: {e}")



# Equipment Model
class Equipment:
    def __init__(self, id, name, model, status, created_at, updated_at):
        self.id = id
        self.name = name
        self.model = model
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

def get_all_equipment():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM equipment")
            equipment_data = cursor.fetchall()
        equipment = [Equipment(*data) for data in equipment_data]
        return equipment
    except Exception as e:
        print(f"Error in get_all_equipment: {e}")
        return []

def get_equipment_by_id(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM equipment WHERE id = %s", (id,))
            equipment_data = cursor.fetchone()
        return Equipment(*equipment_data) if equipment_data else None
    except Exception as e:
        print(f"Error in get_equipment_by_id: {e}")
        return None

def create_equipment(name, model, status):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO equipment (name, model, status) VALUES (%s, %s, %s)",
                           (name, model, status))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in create_equipment: {e}")
        # return None

def update_equipment(id, name, model, status):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE equipment SET name = %s, model = %s, status = %s WHERE id = %s",
                           (name, model, status, id))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in update_equipment: {e}")

def delete_equipment(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM equipment WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in delete_equipment: {e}")


# Samples Model
class Sample:
    def __init__(self, id, name, type, weight, location, date_sampled, sampled_by, created_at, updated_at):
        self.id = id
        self.name = name
        self.type = type
        self.weight = weight
        self.location = location
        self.date_sampled = date_sampled
        self.sampled_by = sampled_by
        self.created_at = created_at
        self.updated_at = updated_at


def get_all_samples():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM samples")
            sample_data = cursor.fetchall()
        samples = [Sample(*data) for data in sample_data]
        return samples
    except Exception as e:
        print(f"Error in get_all_samples: {e}")
        return []

def get_sample_by_id(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM samples WHERE id = %s", (id,))
            sample_data = cursor.fetchone()
        return Sample(*sample_data) if sample_data else None
    except Exception as e:
        print(f"Error in get_sample_by_id: {e}")
        #return None

def create_sample(name, type, weight, location, date_sampled, sampled_by):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO samples (name, type, weight, location, date_sampled, sampled_by) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, type, weight, location, date_sampled, sampled_by))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in create_sample: {e}")

def update_sample(id, name, type, weight, location, date_sampled, sampled_by):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE samples SET name = %s, type = %s, weight = %s, location = %s, date_sampled = %s, sampled_by = %s WHERE id = %s",
                           (name, type, weight, location, date_sampled, sampled_by, id))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in update_sample: {e}")

def delete_sample(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM samples WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in delete_sample: {e}")



# Tests Model
class Test:
    def __init__(self, id, name, type, standard, date_tested, results, tested_by, created_at, updated_at):
        self.id = id
        self.name = name
        self.type = type
        self.standard = standard
        self.date_tested = date_tested
        self.results = results
        self.tested_by = tested_by
        self.created_at = created_at
        self.updated_at = updated_at

def get_all_tests():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tests")
            test_data = cursor.fetchall()
        tests = [Test(*data) for data in test_data]
        return tests
    except Exception as e:
        print(f"Error in get_all_tests: {e}")
        return []

def get_test_by_id(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tests WHERE id = %s", (id,))
            test_data = cursor.fetchone()
        return Test(*test_data) if test_data else None
    except Exception as e:
        print(f"Error in get_test_by_id: {e}")
        return None

def create_test(name, type, standard, date_tested, results, tested_by):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO tests (name, type, standard, date_tested, results, tested_by) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, type, standard, date_tested, results, tested_by))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in create_test: {e}")

def update_test(id, name, type, standard, date_tested, results, tested_by):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE tests SET name = %s, type = %s, standard = %s, date_tested = %s, results = %s, tested_by = %s WHERE id = %s",
                           (name, type, standard, date_tested, results, tested_by, id))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in update_test: {e}")

def delete_test(id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM tests WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in delete_test: {e}")

