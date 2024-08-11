"""
feedback_logic.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: feedback_logic.py
Revised: [Add revised date]

Description:
This module implements the logic for generating feedback for resumes based on the analysis results.

Classes:
    FeedbackGenerator: A class to generate feedback for resumes.

Usage:
    Import this module and use the FeedbackGenerator class to generate feedback for resumes.

Example:
    from feedback_logic import FeedbackGenerator

    analysis_results_example = {
        "matching_skills": {"Python", "Java"},
        "score": 0.75
    }
    generator = FeedbackGenerator()
    feedback = generator.generate_feedback(analysis_results_example)
    print(feedback)
"""

import logging

# Configure logging
logger = logging.getLogger('feedback_logic')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('feedback_logic.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class FeedbackGenerator:
    """
    A class to generate feedback for resumes based on the analysis results.
    """

    @staticmethod
    def generate_feedback(analysis_results: dict) -> dict:
        """
        Generate feedback based on the analysis results.

        Args:
            analysis_results (dict): The results of analyzing the résumé.

        Returns:
            dict: Generated feedback for the résumé.
        """
        try:
            score = analysis_results.get("score", 0)
            matching_skills = analysis_results.get("matching_skills", set())

            feedback_messages = []

            if score > 0.8:
                feedback_messages.append("Your resume is highly relevant to the job description. Great job!")
            elif score > 0.5:
                feedback_messages.append(
                    "Your resume is fairly relevant. Consider highlighting your skills more prominently.")
            else:
                feedback_messages.append(
                    "Your resume has low relevance. "
                    "You may need to improve your resume content to match the job description.")

            if matching_skills:
                feedback_messages.append(f"Matching skills found: {', '.join(matching_skills)}")
            else:
                feedback_messages.append(
                    "No matching skills found. Consider adding more relevant skills to your resume.")

            feedback_result = {
                "strengths": feedback_messages,
                "score": score
            }
            logger.info(f"Generated feedback: {feedback_result}")
            return feedback_result
        except Exception as e:
            logger.error(f"An error occurred while generating feedback: {e}")
            return {"strengths": ["An error occurred while generating feedback."], "score": 0}


# Example usage
if __name__ == "__main__":
    analysis_results_example = {
        "matching_skills": {"Python", "Java"},
        "score": 0.75
    }
    generator = FeedbackGenerator()
    feedback = generator.generate_feedback(analysis_results_example)
    print(feedback)
