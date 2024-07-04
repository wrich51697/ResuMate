"""
Author: William Richmond
Created on: 07 July 2024
File name: resume_routes.py
Revised: 08 July 2024

Description:
This module defines the résumé-related routes for the ResuMate application.
It includes routes for uploading and analyzing resumes.

Usage:
    Import this module and initialize the routes with the given Flask app instance.

Example:
    from resume_routes import resume_bp

    app = Flask(__name__)
    app.register_blueprint(resume_bp)
"""

import os
from io import BytesIO

from docx import Document
from flask import Blueprint, request, send_file, jsonify
from flask_login import login_required
from transformers import pipeline

from app.utils.file_handler import FileHandler

resume_bp = Blueprint('resume', __name__, template_folder='app/templates')

# Load the model and tokenizer
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')


@resume_bp.route('/upload_resume', methods=['GET', 'POST'])
@login_required
def upload_resume():
    return FileHandler.upload(request)


@resume_bp.route('/analyze_resume', methods=['POST'])
@login_required
def analyze_resume():
    resume_file = request.files.get('resume_file')
    job_description = request.form.get('job_description')

    if not resume_file:
        return "Resume file is required", 400

    resume_text = ""
    if resume_file.filename.endswith('.docx'):
        document = Document(BytesIO(resume_file.read()))
        for paragraph in document.paragraphs:
            resume_text += paragraph.text + "\n"
    else:
        resume_text = resume_file.read().decode('utf-8')

    if not resume_text.strip():
        return "Resume text is required", 400

    analysis_result = classifier(resume_text)
    return jsonify(analysis_result), 200


@resume_bp.route('/download_sample_resume')
@login_required
def download_sample_resume():
    sample_resume_path = os.path.join(os.getcwd(), 'app/static/uploads', 'Brian_resume_1.docx')
    return send_file(sample_resume_path, as_attachment=True)
