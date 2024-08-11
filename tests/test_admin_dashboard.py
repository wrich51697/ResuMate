"""
test_admin_dashboard.py
------------------------------------------------
Author: William Richmond
Created on: [Current Date]
File name: test_admin_dashboard.py
Revised: [Add revised date]

Description:
This module contains unit tests for the admin dashboard functionalities of the ResuMate application.
It includes tests for accessing the admin dashboard, user management, resume management, and system logs.

Usage:
    Run this module to execute the unit tests for the admin dashboard functionalities.

Example:
    python test_admin_dashboard.py
"""

from app import create_app
from app.db_manager import DBManager
from app.models import User, Role
from flask_bcrypt import Bcrypt
import unittest
import os
import logging

db_manager = DBManager()
bcrypt = Bcrypt()


class AdminDashboardTest(unittest.TestCase):

    def setUp(self):
        """
        Set up the database and create test data before each test.
        """
        # Ensure template directory is correct
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'templates')
        logging.info(f"Template directory set to: {template_dir}")
        self.app = create_app('testing', template_folder=template_dir)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db = db_manager.get_db()
        db.create_all()
        self.create_test_data()

        # Log in the admin user
        self.login_admin()

    def tearDown(self):
        """
        Clean up the database after each test.
        """
        db = db_manager.get_db()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def create_test_data():
        """
        Create test data for the database.
        """
        db = db_manager.get_db()

        # Create roles
        admin_role = Role(name='Admin')
        db.session.add(admin_role)
        db.session.commit()

        # Create users with hashed passwords
        admin_password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
        user_password_hash = bcrypt.generate_password_hash('password').decode('utf-8')

        admin_user = User(first_name='John', last_name='Doe', username='john', email='john@example.com',
                          password_hash=admin_password_hash, is_active=True)
        regular_user = User(first_name='Jane', last_name='Doe', username='jane', email='jane@example.com',
                            password_hash=user_password_hash, is_active=True)

        db.session.add(admin_user)
        db.session.add(regular_user)
        db.session.commit()

        # Assign role to admin user
        admin_user.roles.append(admin_role)
        db.session.commit()

    def login_admin(self):
        """
        Log in the admin user.
        """
        with self.client:
            response = self.client.post('/login', data=dict(
                email='john@example.com',
                password='password'
            ), follow_redirects=False)
            print(response.data)  # Log response data for debugging
            with self.client.session_transaction() as session:
                flash_messages = dict(session['_flashes']) if '_flashes' in session else {}
            print(flash_messages)  # Log flash messages for debugging
            self.assertEqual(response.status_code, 302)  # Check for redirect
            self.assertIn('/admin/dashboard', response.headers['Location'])  # Ensure redirect to dashboard

    def test_admin_dashboard_access(self):
        """
        Test that the admin dashboard can be accessed by an admin user.
        """
        # Access the admin dashboard
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)  # Check for specific content


if __name__ == '__main__':
    unittest.main()
