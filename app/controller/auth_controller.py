from flask import Blueprint, render_template , request , flash, url_for, redirect
from app.services.user_service import UserService

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

         # Call the service to register the user
        UserService.register_user(username, email, password)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))  # Redirect to login page after registration
    return render_template('register.html')
