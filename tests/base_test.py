"""
base_test.py
------------------------------------------------
Author: William Richmond
Created on: 28 July 2024
File name: base_test.py
Revised: 02 August 2024

Description:
This module provides a base test case for setting up and tearing down the test environment.
It includes setup and teardown methods to initialize and clean up the test environment.

Classes:
    TestBaseTestCase: A base test case class for setting up and tearing down the test environment.

Usage:
    Import this module and inherit from TestBaseTestCase to create test cases with a predefined setup and teardown.

Example:
    from base_test import TestBaseTestCase

    class MyTests(TestBaseTestCase):
        def test_something(self):
            # Your test code here
"""

import unittest
from app import create_app
from app.db_manager import db
from app.log import AppLogger
from app.models import User

# Initialize the logger using AppLogger
test_logger = AppLogger.get_logger()


class TestBaseTestCase(unittest.TestCase):
    """
    A base test case class for setting up and tearing down the test environment.
    """

    def setUp(self):
        """
        Set up the test environment by creating the database and adding a test user.
        """
        test_logger.info("Setting up the test environment")
        try:
            self.app = create_app('testing')
            self.app_context = self.app.app_context()
            self.app_context.push()
            self.client = self.app.test_client()  # Initialize the test client
            db.create_all()

            # Create a test user
            self.create_test_user()

            # Define the sample directory for test files
            self.sample_dir = r'C:\Users\Brian Richmond\PycharmProjects\ResuMate\uploads'
        except Exception as e:
            test_logger.error(f"Error setting up the test environment: {e}")

    def tearDown(self):
        """
        Tear down the test environment by removing the database session and dropping all tables.
        """
        test_logger.info("Tearing down the test environment")
        try:
            db.session.remove()
            db.drop_all()
            self.app_context.pop()
        except Exception as e:
            test_logger.error(f"Error tearing down the test environment: {e}")

    @staticmethod
    def create_test_user():
        """
        Create a test user in the database.
        """
        try:
            user = User(first_name='Test', last_name='User', username='testuser', email='tests@example.com',
                        password_hash='password')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            test_logger.info("Test user created successfully")
        except Exception as e:
            test_logger.error(f"Error creating test user: {e}")

    def login(self):
        """
        Login the test user.
        """
        return self.client.post('/user/login', data=dict(
            email='tests@example.com',
            password='password'
        ), follow_redirects=True)

    def set_user_session(self):
        """
        Set the user session for the test client.
        """
        with self.client.session_transaction() as sess:
            user = User.query.filter_by(email='tests@example.com').first()
            sess['_user_id'] = user.id

    def test_setup(self):
        """
        Test if the setup creates a test user.
        """
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'tests@example.com')
