"""
db_manager.py
------------------------------------------------
Author: William Richmond
Created on: 01 July 2024
File name: db_manager.py
Revised: 14 July 2024

Description:
This module manages the database connection for the Flask application.
It includes methods to initialize and retrieve the SQLAlchemy database instance.

Usage:
    Import this module and create an instance of DBManager.
    Call init_app(app) to initialize the database with the Flask app instance.

Example:
    from db_manager import DBManager

    db_manager = DBManager()
    db_manager.init_app(app)
"""

import logging
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

# Configure logging
logger = logging.getLogger('db_manager')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('db_manager.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class DBManager:
    """
    Class to manage the database connection using SQLAlchemy.

    Methods:
        init_app: Initializes the database with the Flask app instance.
        get_db: Returns the SQLAlchemy database instance.
    """

    def __init__(self, app=None):
        self.db = db
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the database with the Flask app instance.

        Args:
            app (Flask): The Flask application instance.
        """
        self.db.init_app(app)
        logger.info('Database initialized with the Flask app instance')

    def get_db(self):
        """
        Returns the SQLAlchemy database instance.

        Returns:
            SQLAlchemy: The SQLAlchemy database instance.
        """
        return self.db
