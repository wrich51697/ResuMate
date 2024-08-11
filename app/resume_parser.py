import docx2txt
from pdfminer.high_level import extract_text
import logging
import spacy
from spacy.matcher import PhraseMatcher
from typing import Dict, List

# Initialize logger
logger = logging.getLogger('resumate.resume_parser')
logger.setLevel(logging.DEBUG)

# Load SpaCy model
nlp_spacy = spacy.load("en_core_web_lg")


class ResumeParser:
    """
    A class to handle the parsing of resume text using SpaCy.
    """

    @staticmethod
    def extract_text_from_file(resume_file_path: str) -> str:
        """
        Extract text from a given file.

        Args:
            resume_file_path (str): The path to the resume file.

        Returns:
            str: The extracted text from the file.
        """
        try:
            if resume_file_path.endswith('.pdf'):
                return extract_text(resume_file_path)
            elif resume_file_path.endswith('.docx'):
                return docx2txt.process(resume_file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            logger.error(f"An error occurred while extracting text from the file: {e}")
            return ""

    @staticmethod
    def identify_sections(resume_text_content: str) -> Dict[str, str]:
        """
        Identify sections in the resume text.

        Args:
            resume_text_content (str): The resume text.

        Returns:
            dict: A dictionary with identified sections.
        """
        resume_sections: Dict[str, str] = {
            "personal_info": "",
            "experience": "",
            "education": "",
            "skills": "",
            "achievements": "",
            "certifications": "",
            "projects": "",
            "references": "",
            "summary": "",
        }

        section_map = {
            "experience": "experience",
            "education": "education",
            "skills": "skills",
            "achievements": "achievements",
            "accomplishments": "achievements",
            "certifications": "certifications",
            "projects": "projects",
            "references": "references",
            "summary": "summary",
            "profile": "summary",
            "name": "personal_info",
            "email": "personal_info",
            "phone": "personal_info"
        }

        lines = resume_text_content.split('\n')
        current_section = None

        for line in lines:
            line_lower = line.strip().lower()
            section_found = False
            for key, section in section_map.items():
                if line_lower.startswith(f"{key}:"):
                    logger.debug(f"Section key found: {key} in line: {line_lower}")
                    current_section = section
                    section_found = True
                    resume_sections[current_section] += (line.replace(f"{key.capitalize()}:", "")
                                                         .replace(f"{key}:", "").strip() + " ")
                    break

            if not section_found and current_section:
                logger.debug(f"Appending to current_section {current_section}: {line.strip()}")
                resume_sections[current_section] += line.strip() + " "

        for key in resume_sections:
            resume_sections[key] = ' '.join(resume_sections[key].split())
            logger.debug(f"Section {key}: {resume_sections[key]}")

        logger.debug(f"Final sections: {resume_sections}")
        return resume_sections

    @staticmethod
    def setup_phrase_matcher(nlp, phrases: List[str]):
        """
        Set up PhraseMatcher with a list of phrases.

        Args:
            nlp: The SpaCy language model.
            phrases (List[str]): List of phrases to match.

        Returns:
            PhraseMatcher: The configured PhraseMatcher.
        """
        matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(text) for text in phrases]
        matcher.add("PHRASES", patterns)
        return matcher

    @staticmethod
    def parse(resume_text_content: str) -> Dict[str, List[str]]:
        """
        Parse resume text to extract relevant information.

        Args:
            resume_text_content (str): The resume text to parse.

        Returns:
            dict: A dictionary with extracted information.
        """
        try:
            doc_spacy = nlp_spacy(resume_text_content)

            # Define specific phrases to match
            phrases = ["John Doe", "Software Engineer", "Senior Developer", "Python", "Java", "SQL"]
            matcher = ResumeParser.setup_phrase_matcher(nlp_spacy, phrases)
            matches = matcher(doc_spacy)

            matched_phrases = [doc_spacy[start:end].text for match_id, start, end in matches]

            logger.debug(f"Matched phrases: {matched_phrases}")

            return {
                "matched_phrases": matched_phrases
            }
        except Exception as e:
            logger.error(f"An error occurred while parsing the resume: {e}")
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
    Achievements: Developed a new feature that increased user engagement by 20%
    Certifications: AWS Certified Solutions Architect
    Projects: Developed an internal tool for automating deployment
    References: Available upon request
    """
    parsed_data = ResumeParser.parse(resume_text_example)
    print(parsed_data)
