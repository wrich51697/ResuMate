"""
feedback_logic.py
------------------------------------------------
Author: Brian Richmond
Created on: 07 July 2024
File name: feedback_logic.py
Revised:

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


class FeedbackGenerator:
    """
    A class to generate feedback for resumes based on the analysis results.
    """

    @staticmethod
    def generate_feedback(analysis_results):
        """
        Generate feedback based on the analysis results.

        Args:
            analysis_results (dict): The results of analyzing the résumé.

        Returns:
            str: Generated feedback for the résumé.
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

            return " ".join(feedback_messages)
        except Exception as e:
            print(f"An error occurred while generating feedback: {e}")
            return "An error occurred while generating feedback."


# Example usage
if __name__ == "__main__":
    analysis_results_example = {
        "matching_skills": {"Python", "Java"},
        "score": 0.75
    }
    generator = FeedbackGenerator()
    feedback = generator.generate_feedback(analysis_results_example)
    print(feedback)
