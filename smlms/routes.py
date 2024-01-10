from flask import render_template, request, redirect, session, url_for
from smlms import app, mysql
from flask_bcrypt import Bcrypt
import MySQLdb.cursors, re
from smlms.models import create_equipment, create_project, create_sample, create_user, delete_equipment, delete_project_by_id, delete_sample, get_all_equipment, get_all_projects, get_all_samples, get_all_users, get_equipment_by_id, get_project_by_id, get_sample_by_id, get_user_by_email, update_equipment, update_project_by_id, update_sample

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        entered_password = request.form['password']
        user  = get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, entered_password):
            session['loggedin'] = True
            session['userid'] = user.id
            session['name'] = user.name
            session['email'] = user.email
            session['role'] = user.role
            message = 'Logged in successfully!'
            return render_template('profile.html', message=message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('role', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        account = get_user_by_email(email)
        if account:
            message = 'Account already exists !'
        elif not name or not password or not email:
            message = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            create_user(name, email, hashed_password)
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message = message)

@app.route("/dashboard", methods =['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:        
        return render_template("dashboard.html")
    return redirect(url_for('login'))   

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_user_by_id(session['user_id'])
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        update_user_profile(user.id, name, email)
        user = get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/users')
def Index():
    users = get_all_users()
    return render_template('users.html', users=users)





# Route for handling CRUD operations on projects
@app.route('/projects')
def projects():
    # Get all projects
    projects = get_all_projects()
    return render_template('projects.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_details(project_id):
    # Get project details
    project = get_project_by_id(project_id)
    # (Optional) Get associated samples, tests, etc. based on project ID
    return render_template('project_details.html', project=project)

@app.route('/create_project', methods=['GET', 'POST'])
def create_projects():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        budget = request.form.get('budget')
        create_project(name, location, description, start_date, end_date, budget)
        return redirect(url_for('projects'))
    else:
        return render_template('create_project.html')

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    # Get project details
    project = get_project_by_id(project_id)
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        budget = request.form.get('budget')
        update_project_by_id(project_id, name, location, description, start_date, end_date, budget)
        return redirect(url_for('projects'))
    else:
        return render_template('edit_project.html', project=project)

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    try:
        # Assuming you have a function to delete the project by ID
        delete_project_by_id(project_id)
    except Exception as e:
        print(f"Error in delete_project: {e}")
        # Handle the error as needed, e.g., return an error response

    # Redirect to the projects page after deletion
    return redirect(url_for('projects'))








# Route for handling CRUD operations on Equipment
@app.route('/equipment')
def equipment():
    # Get all equipment
    equipment = get_all_equipment()
    return render_template('equipment.html', equipment=equipment)

@app.route('/equipment/<int:equipment_id>')
def equipment_details(equipment_id):
    # Get equipment details
    equipment = get_equipment_by_id(equipment_id)
    # (Optional) Get associated samples, tests, etc. based on project ID
    return render_template('equipment_detail.html', equipment=equipment)

@app.route('/create_equipment', methods=['GET', 'POST'])
def create_equipments():
    if request.method == 'POST':
        name = request.form.get('name')
        model = request.form.get('model')
        status = request.form.get('status')
        create_equipment(name, model, status)
        return redirect(url_for('equipment'))
    else:
        return render_template('create_equipment.html')

@app.route('/edit_equipment/<int:equipment_id>', methods=['GET', 'POST'])
def edit_equipment(equipment_id):
    # Get equipment details
    equipment = get_equipment_by_id(equipment_id)
    if request.method == 'POST':
        name = request.form.get('name')
        model = request.form.get('model')
        status = request.form.get('status')
        update_equipment(equipment_id, name, model, status)
        return redirect(url_for('equipment'))
    else:
        return render_template('edit_equipment.html', equipment=equipment)

@app.route('/delete_equipment/<int:equipment_id>', methods=['POST'])
def delete_equipments(equipment_id):
    try:
        # Assuming you have a function to delete the equipment by ID
        delete_equipment(equipment_id)
    except Exception as e:
        print(f"Error in delete_equipment: {e}")
        # Handle the error as needed, e.g., return an error response
    # Redirect to the equipment page after deletion
    return redirect(url_for('equipment'))






# Route for handling CRUD operations on Samples
@app.route('/samples')
def samples():
    # Get all samples
    samples = get_all_samples()
    return render_template('samples.html', samples=samples)

@app.route('/sample/<int:sample_id>')
def sample_details(sample_id):
    # Get sample details
    sample = get_sample_by_id(sample_id)
    # (Optional) Get associated tests, results, etc. based on sample ID
    return render_template('sample_details.html', sample=sample)

@app.route('/create_sample', methods=['GET', 'POST'])
def create_samples():
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        weight = request.form.get('weight')
        location = request.form.get('location')
        date_sampled = request.form.get('date_sampled')
        sampled_by = request.form.get('sampled_by')
        create_sample(name, type, weight, location, date_sampled, sampled_by)
        return redirect(url_for('samples'))
    else:
        #(Optional) Populate project list dynamically
        projects = get_all_projects()
        return render_template('create_sample.html', projects=projects)

@app.route('/edit_sample/<int:sample_id>', methods=['GET', 'POST'])
def edit_sample(sample_id):
    # Get sample details
    sample = get_sample_by_id(sample_id)
    # (Optional) Populate project list dynamically
    # projects = get_all_projects()
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        weight = request.form.get('weight')
        location = request.form.get('location')
        date_sampled = request.form.get('date_sampled')
        sampled_by = request.form.get('sampled_by')
        update_sample(sample_id, name, type, weight, location, date_sampled, sampled_by)
        return redirect(url_for('samples'))
    else:
        return render_template('edit_sample.html', sample=sample)

@app.route('/delete_sample/<int:sample_id>', methods=['POST'])
def delete_samples(sample_id):
    try:
        # Assuming you have a function to delete the sample by ID
        delete_sample(sample_id)
    except Exception as e:
        print(f"Error in delete_sample: {e}")
        # Handle the error as needed, e.g., return an error response
    # Redirect to the sample page after deletion
    return redirect(url_for('samples'))




@app.route('/tests')
def tests():
    # Get all tests
    tests = get_all_tests()
    return render_template('tests.html', tests=tests)

@app.route('/test/<int:test_id>')
def test_details(test_id):
    # Get test details
    test = get_test_by_id(test_id)
    return render_template('test_details.html', test=test)

@app.route('/create_test', methods=['GET', 'POST'])
def create_test():
    if request.method == 'POST':
        sample_id = request.form.get('sample_id')
        type = request.form.get('type')
        standard = request.form.get('standard')
        date_tested = request.form.get('date_tested')
        results = request.form.get('results')
        observations = request.form.get('observations')
        create_test(sample_id, type, standard, date_tested, results, observations)
        return redirect(url_for('tests'))
    else:
        # (Optional) Populate sample list dynamically
        samples = get_all_samples()
        return render_template('create_test.html', samples=samples)

@app.route('/edit_test/<int:test_id>', methods=['GET', 'POST'])
def edit_test(test_id):
    # Get test details
    test = get_test_by_id(test_id)
    # (Optional) Populate sample list dynamically
    samples = get_all_samples()
    if request.method == 'POST':
        sample_id = request.form.get('sample_id')
        type = request.form.get('type')
        standard = request.form.get('standard')
        date_tested = request.form.get('date_tested')
        results = request.form.get('results')
        observations = request.form.get('observations')
        update_test(test_id, sample_id, type, standard, date_tested, results, observations)
        return redirect(url_for('tests'))
    else:
        return render_template('edit_test.html', test=test, samples=samples)

