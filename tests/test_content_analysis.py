"""
test_content_analysis.py
------------------------------------------------
Author: William Richmond
Created on: 09 July 2024
File name: test_content_analysis.py
Revised: [Add revised date]

Description:
This module contains unit tests for the ContentAnalyzer class implemented in the content_analysis.py module.
The tests verify the functionality of the analysis method, ensuring it correctly matches, and
scores resume keywords against job descriptions.

Classes:
    TestContentAnalyzer: Unit tests for the ContentAnalyzer class.

Usage:
    Run this module with a tests runner to execute the tests.

Example:
    python -m unittest test_content_analysis
"""

import logging
from .base_test import TestBaseTestCase
from app.services.content_analysis import ContentAnalyzer

# Initialize logger
logger = logging.getLogger('resumate.test_content_analysis')


class TestContentAnalyzer(TestBaseTestCase):

    def setUp(self):
        super().setUp()
        logger.info("Setting up the test environment for ContentAnalyzer")
        self.analyzer = ContentAnalyzer()
        self.resume_data = {
            "entities": [],
            "noun_chunks": ["Software Engineer", "Junior Developer", "Python", "Java", "SQL"]
        }
        self.job_description = "Looking for a software engineer with experience in Java, Python, and SQL."

    def test_analyze(self):
        """
        Test the analysis method of the ContentAnalyzer class.
        """
        logger.info("Testing analysis method of ContentAnalyzer")
        try:
            analysis_results = self.analyzer.analyze(self.resume_data, self.job_description)
            expected_matching_hard_skills = {"Java", "Python", "SQL"}
            self.assertIn("matching_hard_skills", analysis_results)
            self.assertEqual(set(analysis_results["matching_hard_skills"]), expected_matching_hard_skills)
            self.assertEqual(analysis_results["score"], 1.0)
        except Exception as e:
            logger.error(f"Error in analysis method test: {e}")
            self.fail("ContentAnalyzer analysis test failed")
