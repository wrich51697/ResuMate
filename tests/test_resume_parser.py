"""
test_resume_parser.py
------------------------------------------------
Author: Brian Richmond
Created on: 09 July 2024
File name: test_resume_parser.py
Revised:

Description:
This module contains unit tests for the ResumeParser class implemented in the resume_parser.py module.
The tests verify the functionality of the parse method,
ensuring it correctly extracts named entities and noun chunks from resume text.

Usage:
    To run the tests, use the following command:
    $ python -m unittest discover tests

Example:
    python -m unittest tests/test_resume_parser.py
"""

import unittest
import sys
import os
from unittest.mock import patch

# Add the parent directory of the app module to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resume_parser import ResumeParser


class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeParser()

    def test_parse(self):
        """
        Test the parse method of the ResumeParser class.
        """
        resume_text = """
        John Doe
        Email: john.doe@example.com

        Experience:
        Software Engineer at ABC Corp
        - Senior Developer at XYZ Inc.

        Skills:
        Python, Java, SQL
        """
        expected_noun_chunks = [
            "John Doe",
            "Software Engineer",
            "Senior Developer",
            "Python",
            "Java",
            "SQL"
        ]
        parsed_data = self.parser.parse(resume_text)
        self.assertEqual(parsed_data["noun_chunks"], expected_noun_chunks)

    @patch('resume_parser.ResumeParser.extract_text_from_file')
    def test_extract_text_from_file(self, mock_extract_text):
        """
        Test the extract_text_from_file method with mocked data.
        """
        mock_extract_text.return_value = """
        John Doe
        Email: john.doe@example.com
        Experience:
        - Software Engineer at ABC Corp
        - Senior Developer at XYZ Inc.
        Skills:
        - Python, Java, SQL
        """

        # Test with mocked data
        extracted_text = self.parser.extract_text_from_file('tests/test_uploads/sample_resume.pdf')
        self.assertIn("John Doe", extracted_text)
        self.assertIn("Software Engineer", extracted_text)
        self.assertIn("Python", extracted_text)

        extracted_text = self.parser.extract_text_from_file('tests/test_uploads/sample_resume.docx')
        self.assertIn("John Doe", extracted_text)
        self.assertIn("Software Engineer", extracted_text)
        self.assertIn("Python", extracted_text)

    def test_identify_sections(self):
        """
        Test the identify_sections method of the ResumeParser class.
        """
        resume_text = """
        Experience:
        - Software Engineer at ABC Corp
        - Senior Developer at XYZ Inc.

        Education:
        - B.S. in Computer Science from University X

        Skills:
        - Python, Java, SQL
        """
        sections = self.parser.identify_sections(resume_text)
        self.assertIn("Software Engineer", sections['experience'])
        self.assertIn("B.S. in Computer Science", sections['education'])
        self.assertIn("Python", sections['skills'])


if __name__ == '__main__':
    unittest.main()
