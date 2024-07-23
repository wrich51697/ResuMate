"""
ai_service.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: ai_service.py
Revised: [Add revised date]

Description:
This module implements the AI service for analyzing resumes.

Classes:
    AIService: A class to handle AI-based analysis of resumes.

Usage:
    Import this module and use the AIService class to perform AI analysis on resumes.

Example:
    from app.services.ai_service import AIService

    ai_service = AIService(model_path='path_to_model')
    analysis_result = ai_service.analyze_resume(resume_text, job_description)
    print(analysis_result)
"""

from transformers import pipeline
from app.services.content_analysis import ContentAnalyzer


class AIService:
    """
    A class to handle AI-based analysis of resumes.
    """

    def __init__(self, model_path: str):
        self.model = pipeline('text-classification', model=model_path)
        self.content_analyzer = ContentAnalyzer()

    def analyze_resume(self, resume_text: str, job_description: str) -> dict:
        """
        Analyze a resume against a job description using both AI model and content analysis.

        Args:
            resume_text (str): The text of the resume.
            job_description (str): The text of the job description.

        Returns:
            dict: The combined analysis results from the AI model and content analysis.
        """
        ai_analysis = self.model(resume_text)
        content_analysis = self.content_analyzer.analyze({"noun_chunks": resume_text.split()}, job_description)

        return {
            "ai_analysis": ai_analysis,
            "content_analysis": content_analysis
        }
