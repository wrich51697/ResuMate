"""
test_feedback_logic.py
------------------------------------------------
Author: Brian Richmond
Created on: 09 July 2024

Description:
This module contains unit test for the FeedbackGenerator class implemented in the feedback_logic.py module.
The test verify the functionality of the generate_feedback method,
 ensuring it provides meaningful feedback based on resume content and job descriptions.

Usage:
    To run the test, use the following command:
    $ python -m unittest discover test

Example:
    python -m unittest test/test_feedback_logic.py
"""

import unittest
from app.feedback_logic import FeedbackGenerator


class TestFeedbackGenerator(unittest.TestCase):
    """
    Unit test for the FeedbackGenerator class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.feedback_generator = FeedbackGenerator()
        self.resume_data = {
            "entities": [],
            "noun_chunks": ["Software Engineer", "Senior Developer", "Python", "Java", "SQL"]
        }
        self.job_description = "We are looking for a Software Engineer with skills in Python, Java, and SQL."

    def test_generate_feedback(self):
        """
        Test the generate_feedback method of the FeedbackGenerator class.
        """
        feedback = self.feedback_generator.generate_feedback(self.resume_data, self.job_description)
        self.assertIn(
            "Your resume matches the following keywords from the job description: software engineer,"
            " python, java, sql.",
            feedback["strengths"])
        self.assertIn("Your resume has a high relevance score.", feedback["strengths"])
        self.assertEqual(feedback["score"], 1.0)


if __name__ == '__main__':
    unittest.main()
