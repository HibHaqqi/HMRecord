from flask import Blueprint, render_template , request , flash, url_for, redirect,session
from app.services.user_service import UserService
import re
from app.controller.equipment_controller import eqp_bp

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

          # Validation checks
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('auth.register'))

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format!', 'danger')
            return redirect(url_for('auth.register'))

        # Check if username or email already exists
        if UserService.user_exists(username, email):
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('auth.register'))

        # Additional password validation (e.g., length)
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return redirect(url_for('auth.register'))

         # Call the service to register the user
        UserService.register_user(username, email, password)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))  # Redirect to login page after registration
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate user credentials
        user = UserService.authenticate_user(email, password)
        if user:
            session['user_id'] = user.id
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('eqp.upload'))  # Redirect to main page after login
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')
