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

from app.log import AppLogger  # Import from app
from app.services.content_analysis import ContentAnalyzer

# Set up logging using AppLogger
logger = AppLogger.get_logger()


class AIService:
    """
    A class to handle AI-based analysis of resumes.
    """

    def __init__(self, model_path: str):
        try:
            self.model = pipeline('text-classification', model=model_path)
            self.content_analyzer = ContentAnalyzer()
            logger.info("AIService initialized successfully with model: %s", model_path)
        except Exception as e:
            logger.error(f"Error initializing AIService with model {model_path}: {e}")
            self.model = None  # Set model to None to indicate failure
            raise

    def analyze_resume(self, resume_text: str, job_description: str) -> dict:
        """
        Analyze a resume against a job description using both AI model and content analysis.

        Args:
            resume_text (str): The text of the resume.
            job_description (str): The text of the job description.

        Returns:
            dict: The combined analysis results from the AI model and content analysis.
        """
        try:
            if not self.model:
                raise ValueError("Model is not loaded")

            logger.debug("Starting resume analysis")
            ai_analysis = self.model(resume_text)
            content_analysis = self.content_analyzer.analyze({"noun_chunks": resume_text.split()}, job_description)

            logger.info("Resume analysis completed successfully")
            return {
                "ai_analysis": ai_analysis,
                "content_analysis": content_analysis
            }
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return {"error": str(e)}
