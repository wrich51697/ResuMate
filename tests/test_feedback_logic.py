"""
test_feedback_logic.py
------------------------------------------------
Author: William Richmond
Created on: 09 July 2024
File name: test_feedback_logic.py
Revised: [Add revised date]

Description:
This module contains unit tests for the FeedbackGenerator class implemented in the feedback_logic.py module.
The tests verify the functionality of the generate_feedback method,
ensuring it provides meaningful feedback based on resume content and job descriptions.

Usage:
    To run the tests, use the following command:
    $ python -m unittest discover tests

Example:
    python -m unittest tests/test_feedback_logic.py
"""

import logging
from .base_test import TestBaseTestCase
from app.feedback_logic import FeedbackGenerator

# Initialize logger
logger = logging.getLogger('resumate.test_feedback_logic')


class TestFeedbackGenerator(TestBaseTestCase):

    def setUp(self):
        super().setUp()
        logger.info("Setting up the test environment")
        self.feedback_generator = FeedbackGenerator()

    def test_generate_feedback(self):
        """
        Test the generate_feedback method of the FeedbackGenerator class.
        """
        try:
            feedback = self.feedback_generator.generate_feedback({
                "score": 1.0,
                "matching_skills": {"software engineer", "python", "java", "sql"}
            })
            strengths = feedback["strengths"]
            expected_matching_skills = {"software engineer", "python", "java", "sql"}
            matching_keywords_text = "Matching skills found: " + ", ".join(sorted(expected_matching_skills))
            relevance_score_text = "Your resume is highly relevant to the job description. Great job!"

            matching_keywords_found = any(set(strength.split(": ")[1].split(", ")) == expected_matching_skills for strength in strengths if "Matching skills found:" in strength)
            relevance_score_found = any(relevance_score_text in strength for strength in strengths)

            self.assertTrue(matching_keywords_found)
            self.assertTrue(relevance_score_found)
            self.assertEqual(feedback["score"], 1.0)
        except Exception as e:
            logger.error(f"Error in test_generate_feedback: {e}")
            self.fail(f"Error in test_generate_feedback: {e}")
