"""
test_basic.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: test_basic.py
Revised: 31 July 2024

Description:
This module contains basic tests for the ResuMate application.
It includes tests for verifying the home page accessibility, user registration,
and user login/logout functionality.

Classes:
    BasicTests: Test case for basic functionality tests.

Usage:
    Run this module with a test runner to execute the tests.

Example:
    python -m unittest test_basic
"""

import logging
import unittest

from tests.base_test import TestBaseTestCase
from app.log import AppLogger

# Initialize logger
app_logger = AppLogger.get_logger()
logger = logging.getLogger('resumate.test_basic')


class BasicTests(TestBaseTestCase):

    def test_home_page(self):
        """
        Test that the home page is accessible.
        """
        logger.info("Testing home page accessibility")
        try:
            response = self.client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome to ResuMate', response.data)
        except Exception as e:
            logger.error(f"Error testing home page accessibility: {e}")
            self.fail("Home page test failed")

    def test_register(self):
        """
        Test user registration functionality.
        """
        # Log out the current user before registering a new one
        self.client.get('/user/logout', follow_redirects=True)

        response = self.client.post('/user/register', data=dict(
            first_name='First', last_name='Last', username='user1', email='user1@example.com', password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Print response data for debugging
        print(response.data.decode())

        # Check for the flash message and dashboard welcome message
        self.assertIn(b'Your account has been created! Welcome to your Dashboard', response.data)
        self.assertIn(b'Welcome to your Dashboard, user1', response.data)

    def test_login_logout(self):
        """
        Test user login and logout functionality.
        """
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to your Dashboard', response.data)
        response = self.client.get('/user/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Check for 'Login' button or link to confirm logout


if __name__ == '__main__':
    unittest.main()
