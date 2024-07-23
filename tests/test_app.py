"""
test_app.py
------------------------------------------------
Author: Brian Richmond
Created on: [Date when the file was created]
File name: test_app.py
Revised:

Description:
This module contains integration tests for the ResuMate application.
It includes tests for user registration, login, logout, file upload, and the user's route.

Classes:
    BasicTests: Test case for the basic functionalities of the ResuMate application.
    UserModelCase: Test case for the User model functionalities.

Usage:
    Run this module with a tests runner to execute the tests.

Example:
    python -m unittest test_app
"""

import unittest
from app import create_app, db
from app.models import User
from app.log import AppLogger

logger = AppLogger.get_logger()


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(first_name='Test', last_name='User', username='testuser', email='tests@example.com',
                        password='password')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

        self.login()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def login(self):
        return self.client.post('/login', data=dict(
            email='tests@example.com',
            password='password'
        ), follow_redirects=True)

    def test_register(self):
        response = self.client.post('/register', data=dict(
            first_name='First', last_name='Last', username='user1', email='user1@example.com', password='password',
            confirm='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

    def test_login_logout(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

    def test_upload_file(self):
        self.login()
        with open('tests/test_resume.txt', 'rb') as resume_file:
            response = self.client.post('/upload', data=dict(
                resume=resume_file
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File successfully uploaded', response.data)

    def test_upload_no_file(self):
        self.login()
        response = self.client.post('/upload', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file part', response.data)

    def test_users(self):
        self.login()
        response = self.client.get('/users', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User List', response.data)


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com', first_name='Susan', last_name='Test', password='password')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com', first_name='John', last_name='Doe', password='password')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))


if __name__ == '__main__':
    unittest.main()
