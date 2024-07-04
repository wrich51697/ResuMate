"""
This module initializes the Flask application along with its extensions and configurations.
It sets up the database, migration tool, bcrypt for hashing, and login management.
Routes and models are also imported and initialized here.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from sqlalchemy.exc import SQLAlchemyError

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class (Config): The configuration class to use.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    try:
        app.config.from_object(config_class)

        # Initialize extensions with the app
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        login_manager.init_app(app)

    except SQLAlchemyError as e:
        # Handle SQLAlchemy initialization errors
        app.logger.error(f"Error initializing SQLAlchemy: {e}")
        raise

    try:
        # Import and initialize routes
        from app import routes
        routes.init_routes(app)

        # Import User model for login management
        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            """
            Load a user by ID.

            Args:
                user_id (int): The ID of the user to load.

            Returns:
                User: The user instance if found, None otherwise.
            """
            return User.query.get(int(user_id))

    except ImportError as e:
        # Handle import errors
        app.logger.error(f"Error importing routes or models: {e}")
        raise

    return app


def app():
    return None
