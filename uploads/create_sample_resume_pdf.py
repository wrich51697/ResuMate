"""
create_sample_resume_pdf.py
------------------------------------------------
Author: Brian Richmond
Created on: 14 July 2024
File name: create_sample_resume_pdf.py
Revised:

Description:
This script creates a sample résumé in PDF format using the fpdf library.
The résumé contains basic details like name, email, experience, and skills.

Usage:
    Run this script to generate a sample resume PDF file.

Example:
    python create_sample_resume_pdf.py
"""

from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


# Create instance of FPDF class
pdf = PDF()

# Add a page
pdf.add_page()

# Set title and body
pdf.chapter_title('John Doe')
pdf.chapter_body(
    'Email: john.doe@example.com\n\nExperience:\n- Software Engineer at ABC Corp\n- Senior Developer at XYZ '
    'Inc.\n\nSkills: Python, Java, SQL')

# Save the pdf with name .pdf
pdf.output('sample_resume.pdf')
