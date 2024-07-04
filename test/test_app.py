"""
Unit tests for the ResuMate Flask application.

This script uses the unittest framework to test the main functionalities of the application,
including the home page and the resume upload feature. It verifies that the routes respond
correctly and handle various scenarios such as missing files and successful file uploads.
"""

import unittest
from app import app


class BasicTests(unittest.TestCase):
    """
    Basic unit tests for the ResuMate application.
    """

    def setUp(self):
        """
        Set up the test client and configure the app for testing.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """
        Test that the home page loads correctly.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resume Upload Form', response.data)

    def test_upload_no_file(self):
        """
        Test that the upload route handles the case where no file is provided.
        """
        response = self.app.post('/upload', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file part', response.data)

    def test_upload_file(self):
        """
        Test that the upload route handles a file upload correctly.
        """
        data = {
            'resume': (open('tests/test_resume.txt', 'rb'), 'test_resume.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'skills', response.data)


if __name__ == "__main__":
    unittest.main()
