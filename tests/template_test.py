"""
template_test.py
------------------------------------------------
Author: William Richmond
Created on: 28 July 2024
File name: template_test.py
Revised:

Description:
This module contains tests for verifying HTML templates in the ResuMate application.

Classes:
    TemplateTestCase: Test case for the HTML templates.

Usage:
    Run this module with a tests runner to execute the tests.

Example:
    python -m unittest template_test
"""

import unittest
from flask import url_for

from app.models import User
from .base_test import TestBaseTestCase


class TemplateTestCase(TestBaseTestCase):
    def setUp(self):
        super().setUp()
        self.app.config['SERVER_NAME'] = 'localhost'  # Set the SERVER_NAME for URL building

    def set_user_session(self):
        """
        Set the user id in session to simulate a logged-in user.
        """
        with self.client.session_transaction() as sess:
            user = User.query.filter_by(username='testuser').first()
            sess['_user_id'] = user.id

    def test_index_template(self):
        with self.app.app_context():
            self.login()
            self.set_user_session()
            response = self.client.get(url_for('user.index'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<title>\n    Home\n - ResuMate</title>', response.data)


if __name__ == '__main__':
    unittest.main()
