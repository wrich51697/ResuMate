"""
This module contains the unit test for the resume parsing functionality.
It verifies that the ResumeParser class correctly parses resumes.
"""

import unittest
from app.resume_parser import ResumeParser


class SpacyTestCase(unittest.TestCase):
    """
    A test case for the ResumeParser class.
    """

    def test_resume_parsing(self):
        """
        Test the resume parsing functionality.
        This test verifies that the ResumeParser class correctly parses a resume
        and extracts the expected entities and noun chunks.
        """
        parser = ResumeParser()
        resume_text = "John Doe, Software Engineer, skills in Python, Java, SQL"
        result = parser.parse(resume_text)
        self.assertIn("entities", result)
        self.assertIn("noun_chunks", result)


if __name__ == '__main__':
    unittest.main()
