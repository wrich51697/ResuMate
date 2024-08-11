"""
test_ai_service.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: test_ai_service.py
Revised:

Description:
This module contains tests for the AI service analysis feature of the ResuMate application.

Classes:
    AIServiceTestCase: Test case for the AI service analysis feature.

Usage:
    Run this module with a tests runner to execute the tests.

Example:
    python -m unittest test_ai_service
"""

import unittest
from unittest.mock import patch
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


class AIServiceTestCase(unittest.TestCase):

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
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            user = MockUser(first_name="Test", last_name="User", username="testuser", email="tests@example.com",
                            password_hash=hashed_password)
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

    @patch('app.services.ai_service.AIService.analyze_resume')
    def test_analyze_resume_docx(self, mock_analyze_resume):
        """
        Test analyzing a DOCX resume file.
        """
        mock_analyze_resume.return_value = {'score': 0.9, 'matching_skills': ['Python', 'Java']}

        with self.client:
            # Login first
            response = self.client.post('/members/login', data=dict(
                email='tests@example.com',
                password='password'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200, "Login failed, cannot proceed with the test")

            # Assuming you have a valid DOCX file to upload for the test
            with open('tests/test_files/sample_resume.docx', 'rb') as docx_file:
                data = {
                    'resume_file': docx_file,
                    'job_description': 'Looking for a Python and Java developer.'
                }
                response = self.client.post('/members/analyze_resume', data=data, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 200)
                self.assertIn('score', response.json)
                self.assertIn('matching_skills', response.json)


if __name__ == '__main__':
    unittest.main()
