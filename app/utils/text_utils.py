"""
text_utils.py
------------------------------------------------
Author: William Richmond
Created on: 28 July 2024
File name: text_utils.py
Revised: [Add revised date]

Description:
This module provides utility functions for text extraction and processing
for the ResuMate application. It includes functions for extracting text
from PDF and DOCX files, and for processing resumes using transformers.

Functions:
    extract_text_from_pdf(file_path): Extracts text from a PDF file.
    extract_text_from_docx(file_path): Extracts text from a DOCX file.
    extract_keywords(text): Extracts keywords from the given text using transformers.
    process_resume(file_path): Processes a resume file to extract keywords.

Usage:
    Import the functions from this module to extract and process text.

Example:
    text = extract_text_from_pdf('resume.pdf')
    keywords = extract_keywords(text)
"""

import os
import logging
from transformers import pipeline
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document

# Configure logging
logger = logging.getLogger('text_utils')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('text_utils.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load pre-trained NLP model from transformers
logger.info("Loading pre-trained NLP model...")
nlp = pipeline("ner", model="bert-base-uncased", tokenizer="bert-base-uncased")


def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.

    Parameters:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """
    try:
        logger.info(f"Extracting text from PDF file: {file_path}")
        return extract_pdf_text(file_path)
    except Exception as e:
        logger.error(f"Error extracting text from PDF file: {e}")
        raise


def extract_text_from_docx(file_path):
    """
    Extracts text from a DOCX file.

    Parameters:
        file_path (str): The path to the DOCX file.

    Returns:
        str: The extracted text from the DOCX file.
    """
    try:
        logger.info(f"Extracting text from DOCX file: {file_path}")
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting text from DOCX file: {e}")
        raise


def extract_keywords(text):
    """
    Extracts keywords from the given text using transformers.

    Parameters:
        text (str): The input text from which to extract keywords.

    Returns:
        list: A list of extracted keywords.
    """
    try:
        logger.info("Extracting keywords from text")
        ner_results = nlp(text)
        keywords = [result['word'] for result in ner_results if result['entity'] == 'LABEL_1']
        logger.info(f"Extracted keywords: {keywords}")
        return keywords
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        raise


def process_resume(file_path):
    """
    Processes a resume file to extract keywords.

    Parameters:
        file_path (str): The path to the resume file.

    Returns:
        list: A list of extracted keywords from the resume.
    """
    try:
        logger.info(f"Processing resume file: {file_path}")
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file type")

        keywords = extract_keywords(text)
        return keywords
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        raise
