"""
__init__.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: __init__.py
Revised: [Add revised date]

Description:
This module initializes the Flask application and integrates various services
such as database, bcrypt, login manager, and AI service.

Functions:
    create_app: Creates and configures the Flask application.

Usage:
    Import the create_app function to initialize the Flask application.

Example:
    from app import create_app
    app = create_app()
"""

from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
from app.db_manager import DBManager
from app.services.ai_service import AIService

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

# Initialize DBManager
db_manager = DBManager()


def create_app(config_name='development'):
    """
    Creates and configures the Flask application.

    Args:
        config_name (str): The configuration name to use (e.g., 'development').

    Returns:
        app (Flask): The configured Flask application.
    """
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db_manager.get_db())

    # Initialize AI service with a valid model
    ai_service = AIService(model_path='distilbert-base-uncased-finetuned-sst-2-english')
    app.ai_service = ai_service

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.Routes.user_routes import user_bp
    from app.Routes.resume_routes import resume_bp

    app.register_blueprint(user_bp, url_prefix='/auth')
    app.register_blueprint(resume_bp, url_prefix='/resume')

    @app.route('/')
    def home():
        return redirect(url_for('auth.index'))

    # Create tables if they do not exist
    with app.app_context():
        db_manager.get_db().create_all()
        print("Database tables created successfully.")

    return app
