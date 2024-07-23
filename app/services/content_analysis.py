"""
content_analysis.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: content_analysis.py
Revised: [Add revised date]

Description:
This module implements content analysis algorithms to score and rank resumes based on relevance.

Classes:
    ContentAnalyzer: A class to handle content analysis of resumes compared to job descriptions.

Usage:
    Import this module and use the ContentAnalyzer class to analyze resume content against job descriptions.

Example:
    from content_analysis import ContentAnalyzer

    resume_data_example = {
        "entities": [],
        "noun_chunks": ["Software Engineer", "Senior Developer", "Python", "Java", "SQL"]
    }
    job_description_example = "We are looking for a Software Engineer with skills in Python, Java, and SQL."
    analyzer = ContentAnalyzer()
    analysis_results = analyzer.analyze(resume_data_example, job_description_example)
    print(analysis_results)
"""


class ContentAnalyzer:
    """
    A class to handle content analysis of resumes compared to job descriptions.
    """

    @staticmethod
    def analyze(resume_data, job_description):
        """
        Analyze the resume content and compare it with the job description.

        Args:
            resume_data (dict): The parsed resume data.
            job_description (str): The job description text.

        Returns:
            dict: Analysis results including scores and matching keywords.
        """
        try:
            # Example analysis: match skills
            resume_skills = {chunk.lower() for chunk in resume_data["noun_chunks"]}
            job_skills = {word.lower() for word in job_description.split()}

            matching_skills = resume_skills.intersection(job_skills)

            score = len(matching_skills) / len(job_skills) if job_skills else 0

            return {
                "matching_skills": list(matching_skills),
                "score": score
            }
        except Exception as e:
            print(f"An error occurred while analyzing the resume: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    resume_data_example = {
        "entities": [],
        "noun_chunks": ["Software Engineer", "Senior Developer", "Python", "Java", "SQL"]
    }
    job_description_example = "We are looking for a Software Engineer with skills in Python, Java, and SQL."
    analyzer = ContentAnalyzer()
    analysis_results = analyzer.analyze(resume_data_example, job_description_example)
    print(analysis_results)
