"""
# csrf_manager.py
------------------------------------------------
Author: William Richmond
Created on: 11 August 2024
File name: csrf_manager.py
Revised: [Add revised date]

Description:
This module manages CSRF protection for the Flask application.
It includes methods to initialize CSRF protection with the Flask app instance.

Usage:
    Import this module and create an instance of CSRFManager.
    Call init_app(app) to initialize CSRF protection with the Flask app instance.

Example:
    from csrf_manager import CSRFManager

    csrf_manager = CSRFManager()
    csrf_manager.init_app(app)
------------------------------------------------
"""

from flask_wtf import CSRFProtect

# Initialize CSRFProtect extension
csrf = CSRFProtect()


class CSRFManager:
    """
    Class to manage CSRF protection using Flask-WTF.

    Methods:
        init_app: Initializes CSRF protection with the Flask app instance.
    """

    def __init__(self):
        self.csrf = csrf

    def init_app(self, app):
        """
        Initializes CSRF protection with the Flask app instance.

        Args:
            app (Flask): The Flask application instance.
        """
        self.csrf.init_app(app)
