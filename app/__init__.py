"""
# __init__.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: __init__.py
Revised: 11 August 2024

Description:
This module initializes the Flask application and integrates various services
such as database, bcrypt, login manager, AI service, and CSRF protection.

Functions:
    create_app: Creates and configures the Flask application.

Usage:
    Import the create_app function to initialize the Flask application.

Example:
    from app import create_app
    app = create_app()
"""

import os
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.auth_manager import AuthManager
from app.db_manager import DBManager
from app.log import AppLogger
from app.services.ai_service import AIService
from app.csrf_manager import CSRFManager  # Import the CSRFManager
from config import config

# Initialize Flask extensions
bcrypt = Bcrypt()
migrate = Migrate()

# Initialize managers
db_manager = DBManager()
auth_manager = AuthManager()
csrf_manager = CSRFManager()  # Initialize CSRFManager

# Initialize the logger using AppLogger
app_logger = AppLogger.get_logger()


def create_app(config_name='development', template_folder=None):
    """
    Creates and configures the Flask application.

    Args:
    config_name (str or Config): The configuration name to use (e.g., 'development', 'testing')
    or a configuration class.
    template_folder (str): Optional path to the template folder.

    Returns:
    app (Flask): The configured Flask application.
    """
    if template_folder is None:
        template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    app = Flask(__name__, template_folder=template_folder)  # Use template_folder variable

    if isinstance(config_name, str):
        app.config.from_object(config[config_name])
        config_obj = config[config_name]
    else:
        app.config.from_object(config_name)
        config_obj = config_name

    config_obj.init_app(app)

    app.config['DEBUG'] = True  # Enable debug mode

    try:
        # Initialize services and extensions
        db_manager.init_app(app)
        bcrypt.init_app(app)
        migrate.init_app(app, db_manager.get_db())
        auth_manager.init_app(app)  # Initialize AuthManager
        csrf_manager.init_app(app)  # Initialize CSRF protection

        # Initialize AI service with a valid model
        ai_service = AIService(model_path='distilbert-base-uncased-finetuned-sst-2-english')
        app.ai_service = ai_service

        from app.models import User

        # Register blueprints for different routes
        from app.routes.admin_routes import admin_bp
        from app.routes.members_routes import members_bp
        from app.routes.public_routes import public_bp

        app.register_blueprint(admin_bp)
        app.register_blueprint(members_bp)
        app.register_blueprint(public_bp)

        @app.route('/')
        def home():
            return redirect(url_for('public.home'))

        # Create tables if they do not exist
        if app.config['TESTING']:
            with app.app_context():
                db_manager.get_db().create_all()
                app_logger.info("Database tables created successfully for testing.")

    except Exception as e:
        app_logger.error(f"Error initializing the app: {e}")

    return app
