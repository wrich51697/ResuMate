"""
test_analyze_resume.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: test_analyze_resume.py
Revised:

Description:
This module contains tests for the resume analysis feature of the ResuMate application.

Classes:
    AnalyzeResumeTests: Test case for the resume analysis feature.

Usage:
    Run this module with a tests runner to execute the tests.

Example:
    python -m unittest test_analyze_resume
"""

import unittest
from flask import Flask
from flask_login import LoginManager, UserMixin
from app.routes.members_routes import members_bp
from app.db_manager import db
from app.auth_manager import bcrypt
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MockUser model setup
Base = declarative_base()


class MockUser(Base, UserMixin):
    __tablename__ = 'mock_user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    username = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    password_hash = Column(String(128))


class AnalyzeResumeTests(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = 'test_uploads'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SECRET_KEY'] = 'supersecretkey'

        self.client = self.app.test_client()

        # Initialize extensions
        db.init_app(self.app)
        bcrypt.init_app(self.app)
        login_manager = LoginManager()
        login_manager.init_app(self.app)

        # Create an in-memory database and add a user
        with self.app.app_context():
            engine = create_engine('sqlite:///:memory:')
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            user = MockUser(first_name="Test", last_name="User", username="testuser", email="tests@example.com",
                            password_hash="hashed_password")
            self.session.add(user)
            self.session.commit()

            @login_manager.user_loader
            def load_user(user_id):
                return self.session.get(MockUser, int(user_id))

            # Log in the tests client
            with self.client.session_transaction() as sess:
                sess['_user_id'] = user.id

        # Initialize routes
        self.app.register_blueprint(members_bp, url_prefix='/members')

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_analyze_resume_no_text(self):
        response = self.client.post('/members/analyze_resume', data={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/members/analyze_resume', data={'resume_file': '', 'job_description': ''})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/members/analyze_resume', data={'resume_file': ' ', 'job_description': ' '})
        self.assertEqual(response.status_code, 400)

    # Add more tests as needed


if __name__ == '__main__':
    unittest.main()
