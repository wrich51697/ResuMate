"""
resume_routes.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: resume_routes.py
Revised: [Add revised date]

Description:
This module defines the résumé-related routes for the ResuMate application.
It includes routes for uploading and analyzing resumes, as well as downloading a sample resume.

Usage:
    Import this module and initialize the routes with the given Flask app instance.

Example:
    from resume_routes import resume_bp

    app = Flask(__name__)
    app.register_blueprint(resume_bp)
"""

import os
from io import BytesIO
from flask import Blueprint, request, send_file, jsonify, current_app
from flask_login import login_required
from docx import Document
from app.utils.file_handler import FileHandler

resume_bp = Blueprint('resume', __name__, template_folder='app/templates')


@resume_bp.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    """
    Handles file uploads for resumes.

    Request Form:
        file: The file to be uploaded.
        user_id: The ID of the user uploading the file.

    Returns:
        JSON response with the upload status and file ID.
    """
    user_id = request.form.get('user_id')
    return FileHandler.upload(request, user_id)


@resume_bp.route('/analyze_resume', methods=['POST'])
@login_required
def analyze_resume():
    """
    Analyze a resume against a job description.

    Request Form:
        resume_file: The resume file to be analyzed.
        job_description: The job description text.

    Returns:
        JSON response with the analysis results.
    """
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

    analysis_result = current_app.ai_service.analyze_resume(resume_text, job_description)
    return jsonify({"analysis_result": analysis_result}), 200


@resume_bp.route('/download_sample_resume')
@login_required
def download_sample_resume():
    """
    Serve a sample resume file for download.

    Returns:
        The sample resume file as an attachment.
    """
    sample_resume_path = os.path.join(os.getcwd(), 'app/static/uploads', 'Brian_resume_1.docx')
    return send_file(sample_resume_path, as_attachment=True)
