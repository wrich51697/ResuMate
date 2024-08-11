"""
public_routes.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: public_routes.py
Revised: [Add revised date]

Description:
This module defines the public-related routes for the ResuMate application.
It includes routes for user registration, login, logout, and other public-facing pages.

Usage:
    Import this module and initialize the routes with the given Flask app instance.

Example:
    from public_routes import public_bp

    app = Flask(__name__)
    app.register_blueprint(public_bp, url_prefix='/public')
"""

import logging

from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from app.auth_manager import bcrypt
from app.db_manager import DBManager
from app.forms import RegistrationForm, LoginForm
from app.log import AppLogger
from app.models import User

# Initialize logger
app_logger = AppLogger.get_logger()
logger = logging.getLogger('resumate.public_routes')

public_bp = Blueprint('public', __name__)

# Initialize DBManager
db_manager = DBManager()
db = db_manager.get_db()


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


@public_bp.route('/')
def home():
    """
    Renders the home page.

    Returns:
        The rendered home.html template.
    """
    return render_template('public/home.html')


@public_bp.route('/about')
def about():
    """
    Renders the about page.

    Returns:
        The rendered about.html template.
    """
    return render_template('public/about.html')


@public_bp.route('/contact')
def contact():
    """
    Renders the contact page.

    Returns:
        The rendered contact.html template.
    """
    return render_template('public/contact.html')


@public_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    Methods:
        GET: Renders the registration form.
        POST: Processes the registration form and creates a new user.

    Returns:
        The registration page or redirects to the login page after successful registration.
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            app_logger.debug('Form validated successfully.')
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                        username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)  # Log in the user directly after registration
            flash('Your account has been created! Welcome to your Dashboard', 'success')
            logger.info(f"User {form.username.data} registered successfully")
            return redirect(url_for('members.member_dashboard'))  # Redirect to the dashboard
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
            db.session.rollback()  # Roll back the transaction on error
    else:
        app_logger.debug('Form errors: %s', form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    app_logger.debug('Form validation failed or method was GET.')
    return render_template('public/register.html', form=form)


@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    Methods:
        GET: Renders the login form.
        POST: Processes the login form and authenticates the user.

    Returns:
        The login page or redirects to the dashboard after successful login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('members.member_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Welcome back', 'success')
                logger.info(f"User {form.email.data} logged in successfully")
                if 'Admin' in [role.name for role in user.roles]:
                    return redirect(url_for('admin.admin_dashboard'))
                return redirect(url_for('members.member_dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            flash('An error occurred during login. Please try again.', 'danger')
    return render_template('public/login.html', title='Login', form=form)


@public_bp.route('/logout')
def logout():
    """
    Handles user logout.

    Returns:
        Redirects to the home page.
    """
    logout_user()
    logger.info(f"User logged out")
    return redirect(url_for('public.home'))


@public_bp.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    """
    Handles the password reset process.

    Methods:
        GET: Renders the password reset form.
        POST: Processes the password reset form and updates the user's password.

    Returns:
        The password reset page or redirects to the login page after a successful reset.
    """
    form = PasswordResetForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password_hash = hashed_password
                db.session.commit()
                flash('Your password has been updated! Please log in with your new password.', 'success')
                return redirect(url_for('public.login'))
            else:
                flash('No account found with that email. Please check and try again.', 'danger')
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            flash('An error occurred during the password reset process. Please try again.', 'danger')
    return render_template('public/password_reset.html', form=form)
