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

import logging

logger = logging.getLogger('resumate')
logger.setLevel(logging.INFO)

HARD_SKILLS = [
    # Programming Languages
    "JavaScript", "Python", "Java", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
    # Web Development
    "HTML", "CSS", "React.js", "Angular", "Vue.js", "Node.js",
    # Database Management
    "SQL", "NoSQL", "MySQL", "PostgreSQL", "MongoDB",
    # Version Control
    "Git", "GitHub", "GitLab", "Bitbucket",
    # Software Development Methodologies
    "Agile", "Scrum", "Kanban", "DevOps",
    # Testing and Debugging
    "Unit Testing", "Integration Testing", "Automated Testing", "Selenium", "JUnit",
    # Cloud Computing
    "AWS", "Amazon Web Services", "Azure", "Google Cloud Platform", "GCP", "Cloud Security",
    # Mobile Development
    "Android Development", "iOS Development", "Flutter", "React Native",
    # Data Structures and Algorithms
    "data structures", "arrays", "linked lists", "trees", "Algorithm design", "Algorithm analysis",
    # Software Design and Architecture
    "Object-Oriented Design", "OOD", "Microservices Architecture", "RESTful API Design",
    # Automation and Scripting
    "Shell Scripting", "PowerShell", "Bash",
    # Security
    "Secure Coding Practices", "Penetration Testing", "Encryption"
]

SOFT_SKILLS = [
    "communication", "effective verbal and written communication", "collaborating", "team members", "stakeholders",
    "clients", "problem-solving", "analyze issues", "develop effective solutions",
    "adaptability", "adjust to new technologies", "methodologies", "project requirements",
    "teamwork", "working well with others", "sharing knowledge", "contributing to a positive team environment",
    "time management", "prioritizing tasks", "meeting deadlines", "managing time effectively",
    "creativity", "innovative thinking", "designing unique solutions", "improving existing systems",
    "attention to detail", "precision in coding", "debugging ensures high-quality software",
    "emotional intelligence", "understanding and managing your own emotions", "empathizing with others",
    "maintaining a harmonious work environment", "critical thinking", "evaluating information",
    "making reasoned decisions", "patience", "staying calm and persistent when facing challenges or complex problems",
    "self-awareness", "recognizing your strengths", "areas for improvement", "personal and professional growth",
    "responsibility", "taking ownership of your work", "being accountable for your actions", "trust and reliability"
]

EDUCATION_KEYWORDS = [
    "B.S.", "Bachelor of Science", "M.S.", "Master of Science",
    "Ph.D.", "Doctor of Philosophy", "Computer Science", "Software Engineering",
    "Bachelor’s Degree in Computer Science", "Bachelor’s Degree in Software Engineering",
    "Bachelor’s Degree in Information Technology", "Bachelor’s Degree in Computer Engineering",
    "Master’s Degree in Computer Science", "Master’s Degree in Software Engineering",
    "Master’s Degree in Information Technology", "Master’s Degree in Computer Engineering",
    "Associate Degree in Computer Science", "Associate Degree in Information Technology",
    "Associate's Degree in Computer Science", "Associate's Degree in Information Technology",
    "A.A.S.", "Associate of Applied Science", "A.S.", "Associate of Science",
    "PhD in Computer Science", "PhD in Software Engineering", "PhD in Information Technology",
    "PhD in Computer Engineering", "Data Science Certification", "Cyber Security Certification",
    "Machine Learning Certification", "Artificial Intelligence Certification",
    "Full Stack Development Bootcamp", "Front-End Development Bootcamp", "Back-End Development Bootcamp",
    "Software Development Bootcamp", "Coding Bootcamp", "Online Courses in Computer Science",
    "Online Courses in Software Development", "Online Courses in Data Science", "Online Courses in Cyber Security",
    "Online Courses in Machine Learning", "Online Courses in Artificial Intelligence",
    "Professional Development in Software Engineering", "Continuing Education in Information Technology",
    "Technical Training in Software Development"
]


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
            resume_text = " ".join(resume_data["noun_chunks"]).lower()
            job_text = job_description.lower()

            def match_keywords(text, keywords):
                return {kw for kw in keywords if kw.lower() in text}

            matching_hard_skills = match_keywords(resume_text, HARD_SKILLS)
            matching_soft_skills = match_keywords(resume_text, SOFT_SKILLS)
            matching_education = match_keywords(resume_text, EDUCATION_KEYWORDS)

            all_keywords = HARD_SKILLS + SOFT_SKILLS + EDUCATION_KEYWORDS
            total_keywords = match_keywords(job_text, all_keywords)

            score = (len(matching_hard_skills | matching_soft_skills | matching_education) /
                     len(total_keywords)) if total_keywords else 0

            logger.info("Content analysis completed successfully")
            return {
                "matching_hard_skills": list(matching_hard_skills),
                "matching_soft_skills": list(matching_soft_skills),
                "matching_education": list(matching_education),
                "score": score
            }
        except Exception as e:
            logger.error(f"An error occurred while analyzing the resume: {e}")
            return {}
