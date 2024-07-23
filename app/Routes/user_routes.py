"""
user_routes.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: user_routes.py
Revised: [Add revised date]

Description:
This module defines the user-related routes for the ResuMate application.
It includes routes for user registration, login, logout, viewing users, viewing user profiles, and file uploads.

Usage:
    Import this module and initialize the routes with the given Flask app instance.

Example:
    from user_routes import user_bp

    app = Flask(__name__)
    app.register_blueprint(user_bp)
"""

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from app.auth_manager import bcrypt, login_manager
from app.db_manager import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app.utils.upload_utils import handle_file_upload

user_bp = Blueprint('auth', __name__)


@user_bp.route('/')
def index():
    return render_template('index.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Welcome back', 'success')
            return redirect(next_page) if next_page else redirect(url_for('auth.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@user_bp.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', title='Users', users=all_users)


@user_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)


@user_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Handles file uploads from users.

    Request Form:
        file: The file to be uploaded.
        user_id: The ID of the user uploading the file.

    Returns:
        JSON response with the upload status and file ID.
    """
    return handle_file_upload()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
