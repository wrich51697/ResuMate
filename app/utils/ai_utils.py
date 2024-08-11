"""
ai_utils.py
------------------------------------------------
Author: William Richmond
Created on: 08 July 2024
File name: transformers.py
Revised: [Add revised date]

Description:
This module loads a pre-trained BERT model and tokenizer for named entity recognition (NER)
and provides a function to extract keywords from text.

Functions:
    extract_keywords: Extracts keywords from text using a pre-trained BERT model for NER.

Usage:
    Import this module and use the extract_keywords function to extract keywords from text.

Example:
    keywords = extract_keywords("Sample text for keyword extraction.")
    print(keywords)
"""

import logging
from transformers import BertTokenizer, BertForTokenClassification, pipeline

# Configure logging
logger = logging.getLogger('transformers')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('transformers.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load pre-trained model and tokenizer
logger.info("Loading pre-trained model and tokenizer...")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Create a pipeline for named entity recognition (NER)
logger.info("Creating NER pipeline...")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)


def extract_keywords(text):
    """
    Extracts keywords from text using a pre-trained BERT model for NER.

    Args:
        text (str): The input text.

    Returns:
        list: A list of extracted keywords.
    """
    logger.info(f"Extracting keywords from text: {text}")
    ner_results = nlp(text)
    keywords = [result['word'] for result in ner_results if result['entity'] == 'LABEL_1']
    logger.info(f"Extracted keywords: {keywords}")
    return keywords
