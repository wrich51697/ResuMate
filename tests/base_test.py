"""
base_test.py
------------------------------------------------
Author: Brian Richmond
Created on: [Date when the file was created]
File name: base_test.py
Revised:

Description:
This module provides a base tests case for the ResuMate application.
It includes setup and teardown methods to initialize and clean up the tests environment.

Classes:
    TestBaseTestCase: A base tests case class for setting up and tearing down the tests environment.

Usage:
    Import this module and inherit from TestBaseTestCase to create tests cases with a predefined setup and teardown.

Example:
    from base_test import TestBaseTestCase

    class MyTests(TestBaseTestCase):
        def test_something(self):
            # Your tests code here
"""

import unittest
from app import create_app
from app.db_manager import db
from app.models import User


class TestBaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the tests environment by creating the database and adding a tests user.
        """
        self.app = create_app('config.TestingConfig')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(first_name='Test', last_name='User', username='testuser', email='tests@example.com',
                        password='password')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the tests environment by removing the database session and dropping all tables.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_setup(self):
        """
        Test if the setup creates a tests user.
        """
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'tests@example.com')


if __name__ == '__main__':
    unittest.main()
