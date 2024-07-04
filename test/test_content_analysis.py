"""
test_content_analysis.py
------------------------------------------------
Author: Brian Richmond
Created on: 09 July 2024

Description:
This module contains unit test for the ContentAnalyzer class implemented in the content_analysis.py module.
The test verify the functionality of the analysis method, ensuring it correctly matches, and
 scores resume keywords against job descriptions.

Usage:
    To run the test, use the following command:
    $ python -m unittest discover test

Example:
    python -m unittest test/test_content_analysis.py
"""

import unittest
from app.content_analysis import ContentAnalyzer


class TestContentAnalyzer(unittest.TestCase):
    """
    Unit test for the ContentAnalyzer class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.analyzer = ContentAnalyzer()
        self.resume_data = {
            "entities": [],
            "noun_chunks": ["Software Engineer", "Senior Developer", "Python", "Java", "SQL"]
        }
        self.job_description = "We are looking for a Software Engineer with skills in Python, Java, and SQL."

    def test_analyze(self):
        """
        Test the analysis method of the ContentAnalyzer class.
        """
        analysis_results = self.analyzer.analyze(self.resume_data, self.job_description)
        expected_matching_keywords = {"software engineer", "python", "java", "sql"}
        self.assertEqual(analysis_results["matching_keywords"], expected_matching_keywords)
        self.assertEqual(analysis_results["score"], 1.0)


if __name__ == '__main__':
    unittest.main()
