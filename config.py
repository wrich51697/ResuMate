"""
config.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: config.py
Revised: 23 July 2024

Description:
This module defines the configuration settings for the Flask application.
It includes various configuration classes to manage settings for different environments such as
development, testing, and production.
The settings include database connection details,
session management, and other application-specific configurations.

Classes:
    Config: Base configuration class containing default settings and methods.
    DevelopmentConfig: Configuration class for development environment, inherited from Config.
    TestingConfig: Configuration class for testing environment, inherited from Config.

Usage:
    Import the desired configuration class and apply it to the Flask application.

Example:
    from flask import Flask
    from config import config

    app = Flask(__name__)
    config_name = 'development' # or 'testing', based on the environment
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
"""

import os
import logging
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger('config')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(os.path.join(log_dir, 'config.log'))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Config:
    """
    Base configuration class containing default settings and methods.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    try:
        database_url = URL.create(
            "mssql+pyodbc",
            username="",  # Add if needed
            password="",  # Add if needed
            host="BRIANS-DESKTOP",
            database="ResuMate",
            query={
                "driver": "ODBC Driver 18 for SQL Server",
                "Trusted_Connection": "yes",
                "TrustServerCertificate": "yes"  # Bypass SSL certificate validation
            }
        )
        SQLALCHEMY_DATABASE_URI = database_url
    except SQLAlchemyError as e:
        logger.error(f"Error creating database URL: {e}")
        SQLALCHEMY_DATABASE_URI = None

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SESSION_TYPE = "filesystem"
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Configuration class for development environment, inherited from Config.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configuration class for testing environment, inherited from Config.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Ensure the path to the upload folder exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)
