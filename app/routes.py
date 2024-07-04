"""
This module defines the routes for the ResuMate application.
It includes routes for user registration, login, logout, viewing users, and user profiles.
"""

from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import text  # Import text for raw SQL execution
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError for exception handling
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User


def init_routes(app):
    """
    Initialize the routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.route('/')
    def index():
        """
        Render the home page.

        Returns:
            str: The rendered HTML template for the home page.
        """
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Handle user registration.

        Returns:
            str: The rendered HTML template for the registration page or a redirect to the login page.
        """
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password_hash=hashed_password
                )
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created! You are now able to log in', 'success')
                return redirect(url_for('login'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'An error occurred: {e}', 'danger')
        return render_template('register.html', title='Register', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Handle user login.

        Returns:
            str: The rendered HTML template for the login page or a redirect to the next page or home page.
        """
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            try:
                user = User.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                    login_user(user, remember=form.remember.data)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('index'))
                else:
                    flash('Login Unsuccessful. Please check email and password', 'danger')
            except SQLAlchemyError as e:
                flash(f'An error occurred: {e}', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.route('/logout')
    def logout():
        """
        Handle user logout.

        Returns:
            str: A redirect to the home page.
        """
        logout_user()
        return redirect(url_for('index'))

    @app.route('/users')
    @login_required
    def users():
        """
        Display a list of all users.

        Returns:
            str: The rendered HTML template for the user's page.
        """
        try:
            users = User.query.all()
            return render_template('users.html', title='Users', users=users)
        except SQLAlchemyError as e:
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('index'))

    @app.route('/test_db')
    def test_db():
        """
        Test the database connection.

        Returns:
            str: A message indicating whether the database connection was successful or not.
        """
        try:
            result = db.session.execute(text('SELECT 1'))
            return "Database connection successful!"
        except SQLAlchemyError as e:
            return f"Database connection failed: {e}"

    @app.route('/user/<int:user_id>')
    @login_required
    def user_profile(user_id):
        """
        Display the profile of a specific user.

        Args:
            user_id (int): The ID of the user to display.

        Returns:
            str: The rendered HTML template for the user profile page or a 404 error if the user is not found.
        """
        try:
            user = User.query.get_or_404(user_id)
            return render_template('user_profile.html', title=f'{user.username}\'s Profile', user=user)
        except SQLAlchemyError as e:
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('users'))
