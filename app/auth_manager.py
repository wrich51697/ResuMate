"""
auth_manager.py
------------------------------------------------
Author: William Richmond
Created on: 13 July 2024
File name: auth_manager.py
Revised: [Date when the file was revised]

Description:
This module manages authentication for the Flask application.
It includes methods to initialize bcrypt and login manager with the Flask app instance.

Usage:
    Import this module and create an instance of AuthManager.
    Call init_app(app) to initialize the authentication with the Flask app instance.

Example:
    from auth_manager import AuthManager

    auth_manager = AuthManager()
    auth_manager.init_app(app)
"""

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models import User

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()


class AuthManager:
    """
    Class to manage authentication using bcrypt and Flask-Login.

    Methods:
        init_app: Initializes bcrypt and login manager with the Flask app instance.
        get_bcrypt: Returns the bcrypt instance.
        get_login_manager: Returns the login manager instance.
    """
    def __init__(self):
        self.bcrypt = bcrypt
        self.login_manager = login_manager
        self.login_manager.login_view = 'auth.login'
        self.login_manager.login_message_category = 'info'

    def init_app(self, app):
        self.bcrypt.init_app(app)
        self.login_manager.init_app(app)

        # Define user loader callback
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    def get_bcrypt(self):
        return self.bcrypt

    def get_login_manager(self):
        return self.login_manager
