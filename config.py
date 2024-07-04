import os
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


class Config:
    """
    Base configuration class containing default settings and methods.
    """

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    try:
        # Database connection URL using SQLAlchemy
        database_url = URL.create(
            "mssql+pyodbc",
            host="BRIANS-DESKTOP",  # Use the default instance instead of SQLEXPRESS
            database="ResuMate",
            query={"driver": "ODBC Driver 17 for SQL Server", "Trusted_Connection": "yes"}
        )
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or str(database_url)
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-specific errors
        print(f"Error creating database URL: {e}")
        SQLALCHEMY_DATABASE_URI = None

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Session type for Flask sessions
    SESSION_TYPE = "filesystem"

    @staticmethod
    def init_app(app):
        """
        Initialize the application with the given configuration.

        Args:
            app (Flask): The Flask application instance.
        """
        pass


class DevelopmentConfig(Config):
    """
    Development configuration class.
    Inherits from the base Config class and sets development-specific settings.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration class.
    Inherits from the base Config class and sets testing-specific settings.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite database for testing
    WTF_CSRF_ENABLED = False


# Configuration dictionary to map configuration names to classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
