# test_basic.py

import unittest
from app import create_app, db
from config import TestingConfig


class BasicTests(unittest.TestCase):

    def setUp(self):
        """
        Set up the tests client and initialize the application with the TestConfig.
        """
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Tear down the tests client and remove the application context.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """
        Test that the home page is accessible.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to ResuMate', response.data)


if __name__ == '__main__':
    unittest.main()
