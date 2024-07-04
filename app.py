from flask import Flask, session, request, redirect, url_for, render_template
import sqlite3
from functools import wraps

app = Flask(__name__)

# Set the secret key to a random value
app.secret_key = b'3a98b16f2a8e4c7e71a72e72303bf22b'

# Function to connect to SQLite database
def connect_db():
    conn = sqlite3.connect('db/db/database.db')
    return conn

# Decorator to check if the user is admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('role') != 'admin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if the user is student
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('role') != 'student':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# User Login route
@app.route('/login', methods=['POST', 'GET'])
def student_login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        
        # Connect to database
        conn = connect_db()
        cursor = conn.cursor()

        # Query database for user with matching phone and password
        query = "SELECT * FROM student WHERE phone = ? AND password = ?"
        cursor.execute(query, (phone, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[3]  # Assuming 'email' column as username for session
            session['user_id'] = user[0]   # Assuming 'id' column as user_id for session
            session['role'] = 'student'    # Set role as student
            conn.close()
            return redirect(url_for('user_dashboard'))
        else:
            conn.close()
            return "Invalid phone number or password. Please try again."

    return render_template('index.html')

@app.route('/user/dashboard')
@student_required
def user_dashboard():
    if 'username' in session:         
        return render_template('user/dashboard.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('index'))

# Admin Login route
@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        
        # Connect to database
        conn = connect_db()
        cursor = conn.cursor()

        # Query database for admin with matching phone and password
        query = "SELECT * FROM admin WHERE phone = ? AND password = ?"
        cursor.execute(query, (phone, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[3]  # Assuming 'email' column as username for session
            session['user_id'] = user[0]   # Assuming 'id' column as user_id for session
            session['role'] = 'admin'      # Set role as admin
            conn.close()
            return redirect(url_for('admin_dashboard'))
        else:
            conn.close()
            return "Invalid phone number or password. Please try again."

    return render_template('index.html')

# Admin dashboard route
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    if 'username' in session:         
        return render_template('admin/admin_dashboard.html', username=session['username'])
    return redirect(url_for('index'))

# Add student route for admin
@app.route('/admin/add_student')
@admin_required
def add_student():
    if 'username' in session:         
        return render_template('admin/add_student.html', username=session['username'])
    return redirect(url_for('index'))

# Insert student details from form
@app.route('/insert_student', methods=['POST'])
@admin_required
def insert_student():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        class_name = request.form['class']
        roll_no = request.form['roll']

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO student (name, dob, email, phone, class, password, roll) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, dob, email, phone, class_name, password, roll_no)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('error'))

    return render_template('insert_student.html')

# Add student route for admin
@app.route('/admin/add_admin')
@admin_required
def add_admint():
    if 'username' in session:         
        return render_template('admin/add_admin.html', username=session['username'])
    return redirect(url_for('index'))

# Insert Admin details from form
@app.route('/insert_admin', methods=['POST'])
@admin_required
def insert_admin():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO admin (name, dob, email, phone, password) VALUES (?, ?, ?, ?, ?)',
                (name, dob, email, phone, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('error'))

    return render_template('insert_student.html')

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Error route
@app.route('/error')
def error():
    return "An error occurred. Please try again."

# Run app
if __name__ == '__main__':
    app.run(debug=True)
