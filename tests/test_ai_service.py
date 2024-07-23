"""
test_ai_service.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: test_ai_service.py
Revised: [Add revised date]

Description:
This module contains unit tests for the AIService and related API endpoints.
It includes tests for uploading resumes, analyzing resumes, and validating AI analysis results.

Usage:
    Run this module to execute all unit tests.

Example:
    python -m unittest test_ai_service.py
"""

import unittest
from unittest.mock import patch, Mock
from io import BytesIO
from flask import Flask, current_app
from flask_login import LoginManager, UserMixin
from app import create_app, db_manager
from app.models import User, UploadedFile, AIResult
from app.services.ai_service import AIService


class AIServiceTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db_manager.get_db().create_all()

        self.user = User(first_name='Test', last_name='User', username='testuser', email='testuser@example.com',
                         password_hash='hashedpassword')
        db_manager.get_db().session.add(self.user)
        db_manager.get_db().session.commit()

        login_manager = LoginManager()
        login_manager.init_app(self.app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    def tearDown(self):
        """
        Clean up the test environment.
        """
        db_manager.get_db().session.remove()
        db_manager.get_db().drop_all()
        self.app_context.pop()

    def test_upload_resume(self):
        """
        Test uploading a resume file.
        """
        with self.client:
            self.client.post('/auth/login', data=dict(
                email='testuser@example.com',
                password='hashedpassword'
            ))

            data = {
                'file': (BytesIO(b'fake resume content'), 'resume.docx'),
                'user_id': self.user.id
            }
            response = self.client.post('/resume/upload_resume', content_type='multipart/form-data', data=data)

            self.assertEqual(response.status_code, 201)
            json_response = response.get_json()
            self.assertIn('file_id', json_response)

            uploaded_file = UploadedFile.query.get(json_response['file_id'])
            self.assertIsNotNone(uploaded_file)
            self.assertEqual(uploaded_file.filename, 'resume.docx')

    @patch('app.services.ai_service.AIService.analyze_resume')
    def test_analyze_resume(self, mock_analyze_resume):
        """
        Test analyzing a resume file.
        """
        mock_analyze_resume.return_value = {'score': 0.9, 'matching_skills': ['Python', 'Java']}

        with self.client:
            self.client.post('/auth/login', data=dict(
                email='testuser@example.com',
                password='hashedpassword'
            ))

            data = {
                'resume_file': (BytesIO(b'fake resume content'), 'resume.docx'),
                'job_description': 'We need a Python developer with Java skills'
            }
            response = self.client.post('/resume/analyze_resume', content_type='multipart/form-data', data=data)

            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('analysis_result', json_response)
            self.assertEqual(json_response['analysis_result']['score'], 0.9)
            self.assertIn('Python', json_response['analysis_result']['matching_skills'])


if __name__ == '__main__':
    unittest.main()
