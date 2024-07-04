"""
resume_parser.py
------------------------------------------------
Author: Brian Richmond
Created on: 07 July 2024
File name: resume_parser.py
Revised:

Description:
This module uses spaCy to parse and extract relevant information from resumes.
It includes a class to handle the parsing of resume text and extract named entities and noun chunks.

Classes:
    ResumeParser: A class to handle the parsing of resume text using spaCy.

Usage:
    Import this module and use the ResumeParser class to parse resume text and extract relevant information.

Example:
    from resume_parser import ResumeParser

    resume_text_example = '''
    John Doe
    Email: john.doe@example.com
    Experience:
    - Software Engineer at ABC Corp
    - Senior Developer at XYZ Inc.
    Skills: Python, Java, SQL
    '''
    parser = ResumeParser()
    parsed_data = parser.parse(resume_text_example)
    print(parsed_data)
"""

import spacy
from textblob import TextBlob
import docx2txt
from pdfminer.high_level import extract_text
import re
import nltk

# Ensure required NLTK resources are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class ResumeParser:
    """
    A class to handle the parsing of resume text using spaCy.
    """

    def __init__(self):
        """
        Initialize the ResumeParser class.

        This method loads the small English model from spaCy.
        """
        self.nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def extract_text_from_file(file_path):
        """
        Extract text from a given file.

        Args:
            file_path (str): The path to the resume file.

        Returns:
            str: The extracted text from the file.
        """
        try:
            if file_path.endswith('.pdf'):
                return extract_text(file_path)
            elif file_path.endswith('.docx'):
                return docx2txt.process(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            print(f"An error occurred while extracting text from the file: {e}")
            return ""

    @staticmethod
    def identify_sections(text):
        """
        Identify sections in the resume text.

        Args:
            text (str): The resume text.

        Returns:
            dict: A dictionary with identified sections.
        """
        sections = {
            "experience": None,
            "education": None,
            "skills": None
        }
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'experience', line, re.IGNORECASE):
                sections['experience'] = "\n".join(lines[i:i + 10])
            elif re.search(r'education', line, re.IGNORECASE):
                sections['education'] = "\n".join(lines[i:i + 10])
            elif re.search(r'skills', line, re.IGNORECASE):
                sections['skills'] = "\n".join(lines[i:i + 10])
        return sections

    @staticmethod
    def check_grammar_spelling(text):
        """
        Check and correct grammar and spelling in the text.

        Args:
            text (str): The text to check.

        Returns:
            str: The corrected text.
        """
        try:
            blob = TextBlob(text)
            return str(blob.correct())
        except Exception as e:
            print(f"An error occurred while checking grammar and spelling: {e}")
            return text

    def analyze_keywords(self, text, keywords):
        """
        Analyze keyword frequency in the text.

        Args:
            text (str): The text to analyze.
            keywords (list): List of keywords to check.

        Returns:
            dict: A dictionary with keyword frequencies.
        """
        try:
            doc = self.nlp(text)
            word_freq = {}
            for token in doc:
                if token.text.lower() in keywords:
                    if token.text.lower() not in word_freq:
                        word_freq[token.text.lower()] = 1
                    else:
                        word_freq[token.text.lower()] += 1
            return word_freq
        except Exception as e:
            print(f"An error occurred while analyzing keywords: {e}")
            return {}

    def generate_feedback(self, sections, keywords):
        """
        Generate feedback based on sections and keyword analysis.

        Args:
            sections (dict): The identified sections in the résumé.
            Keywords (list): List of keywords to check.

        Returns:
            list: A list of feedback strings.
        """
        feedback = []

        # Grammar and Spelling Feedback
        for section, content in sections.items():
            if content:
                corrected_content = self.check_grammar_spelling(content)
                if corrected_content != content:
                    feedback.append(f"Grammar and spelling corrections needed in {section} section.")

        # Section Feedback
        for section, content in sections.items():
            if not content:
                feedback.append(f"Missing {section} section.")

        # Keyword Feedback
        all_text = "\n".join(sections.values())
        keyword_freq = self.analyze_keywords(all_text, keywords)
        for keyword in keywords:
            if keyword not in keyword_freq:
                feedback.append(f"Keyword '{keyword}' is missing.")

        return feedback

    def parse(self, text):
        """
        Parse resume text to extract relevant information.

        Args:
            text (str): The resume text to parse.

        Returns:
            dict: A dictionary with extracted information.
        """
        try:
            doc = self.nlp(text)

            # Extracting named entities (e.g., names, organizations)
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            # Extracting noun chunks (e.g., skills, experience)
            unwanted_keywords = ['Email', 'Experience', 'Skills']
            noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks]

            # Remove unwanted keywords and non-relevant chunks
            cleaned_noun_chunks = []
            for chunk in noun_chunks:
                if any(keyword in chunk for keyword in unwanted_keywords):
                    continue
                # Avoid chunks that are part of email addresses or contain job locations
                if '@' in chunk or ' at ' in chunk:
                    continue
                cleaned_noun_chunks.append(chunk)

            # Add names explicitly if they were missed in noun chunks
            name = next((ent.text for ent in doc.ents if ent.label_ == 'PERSON'), None)
            if name and name not in cleaned_noun_chunks:
                cleaned_noun_chunks.insert(0, name)

            return {
                "entities": entities,
                "noun_chunks": cleaned_noun_chunks
            }
        except Exception as e:
            print(f"An error occurred while parsing the resume: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    resume_text_example = """
    John Doe
    Email: john.doe@example.com
    Experience:
    - Software Engineer at ABC Corp
    - Senior Developer at XYZ Inc.
    Skills: Python, Java, SQL
    """
    parser = ResumeParser()
    parsed_data = parser.parse(resume_text_example)
    print(parsed_data)

    file_path = 'resume.pdf'  # Provide the path to your resume file
    keywords = ['python', 'machine learning', 'data analysis']

    # Extract text from file
    resume_text = parser.extract_text_from_file(file_path)

    # Identify sections in the résumé
    sections = parser.identify_sections(resume_text)

    # Generate feedback based on analysis
    feedback = parser.generate_feedback(sections, keywords)

    # Display feedback
    for item in feedback:
        print(item)
