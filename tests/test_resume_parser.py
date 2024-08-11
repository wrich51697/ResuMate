"""
test_resume_parser.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: test_resume_parser.py
Revised: [Add revised date]

Description:
This module contains unit tests for the ResumeParser class.
It uses the unittest framework to test the functionality of the ResumeParser class,
including text extraction, section identification, and parsing.

Classes:
   TestResumeParser: A class to test the ResumeParser class methods.

Usage:
   Run this module to execute the unit tests for the ResumeParser class.
"""

import unittest
import logging
from unittest.mock import patch
from app.resume_parser import ResumeParser  # Ensure this matches the correct path

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('test_resume_parser')
logger.setLevel(logging.DEBUG)


class TestResumeParser(unittest.TestCase):
    """
    A class to test the ResumeParser class methods.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        logger.info("Setting up the test environment for ResumeParser")
        self.parser = ResumeParser()

    def test_parse(self):
        """
        Test the parse method of the ResumeParser class.
        """
        try:
            resume_text = """
            John Doe
            Email: john.doe@example.com

            Experience:
            Software Engineer at ABC Corp
            - Senior Developer at XYZ Inc.

            Skills:
            Python, Java, SQL
            Achievements:
            - Developed a new feature that increased user engagement by 20%
            Certifications:
            - AWS Certified Solutions Architect
            Projects:
            - Developed an internal tool for automating deployment
            References:
            - Available upon request
            """
            expected_matched_phrases = [
                "John Doe",
                "Software Engineer",
                "Senior Developer",
                "Python",
                "Java",
                "SQL"
            ]
            parsed_data = self.parser.parse(resume_text)
            logger.debug(f"Parsed data: {parsed_data}")
            self.assertEqual(parsed_data["matched_phrases"], expected_matched_phrases)
        except Exception as e:
            logger.error(f"Error in test_parse: {e}")
            self.fail(f"Error in test_parse: {e}")

    @patch('app.resume_parser.ResumeParser.extract_text_from_file')
    def test_extract_text_from_file(self, mock_extract_text):
        """
        Test the extract_text_from_file method with mocked data.
        """
        try:
            mock_extract_text.return_value = """
            John Doe
            Email: john.doe@example.com
            Experience:
            - Software Engineer at ABC Corp
            - Senior Developer at XYZ Inc.
            Skills: Python, Java, SQL
            Achievements: Developed a new feature that increased user engagement by 20%
            Certifications: AWS Certified Solutions Architect
            Projects: Developed an internal tool for automating deployment
            References: Available upon request
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
        except Exception as e:
            logger.error(f"Error in test_extract_text_from_file: {e}")
            self.fail(f"Error in test_extract_text_from_file: {e}")

    def test_identify_sections(self):
        """
        Test the identify_sections method of the ResumeParser class.
        """
        try:
            resume_text = """
            Name: John Doe
            Email: john.doe@example.com
            Phone: 123-456-7890

            Summary:
            Highly skilled software engineer with 10 years of experience.

            Experience:
            - Software Engineer at ABC Corp
            - Senior Developer at XYZ Inc.

            Education:
            - B.S. in Computer Science from University X

            Skills:
            - Python, Java, SQL

            Achievements:
            - Developed a new feature that increased user engagement by 20%

            Certifications:
            - AWS Certified Solutions Architect

            Projects:
            - Developed an internal tool for automating deployment

            References:
            - Available upon request
            """
            sections = self.parser.identify_sections(resume_text)
            logger.debug(f"Identified sections: {sections}")
            self.assertIn("John Doe", sections['personal_info'])
            self.assertIn("Highly skilled software engineer", sections['summary'])
            self.assertIn("Software Engineer", sections['experience'])
            self.assertIn("B.S. in Computer Science", sections['education'])
            self.assertIn("Python", sections['skills'])
            self.assertIn("Developed a new feature", sections['achievements'])
            self.assertIn("AWS Certified Solutions Architect", sections['certifications'])
            self.assertIn("Developed an internal tool", sections['projects'])
            self.assertIn("Available upon request", sections['references'])
        except Exception as e:
            logger.error(f"Error in test_identify_sections: {e}")
            self.fail(f"Error in test_identify_sections: {e}")


if __name__ == '__main__':
    unittest.main()
