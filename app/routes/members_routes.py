"""
members_routes.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: members_routes.py
Revised: [Add revised date]

Description:
This module defines the member-related routes for the ResuMate application.
It includes routes for uploading and analyzing resumes, as well as viewing
user profiles and dashboard.

Usage:
    Import this module and initialize the routes with the given Flask app instance.

Example:
    from member_routes import members_bp

    app = Flask(__name__)
    app.register_blueprint(members_bp, url_prefix='/members')
"""

import logging
import os
from io import BytesIO
from docx import Document
from flask import Blueprint, request, send_file, jsonify, current_app
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app.auth_manager import login_manager
from app.models import User
from app.utils.file_handler import FileHandler

members_bp = Blueprint('members', __name__, template_folder='app/templates/members')

# Initialize logger
logger = logging.getLogger('resumate.member_routes')


@members_bp.route('/dashboard')
@login_required
def member_dashboard():
    """
    Renders the member dashboard.

    Returns:
        The rendered admin_dashboard.html template.
    """
    return render_template('members/member_dashboard.html')


@members_bp.route('/profile')
@login_required
def member_profile():
    """
    Renders the member profile page.

    Returns:
        The rendered user_profile.html template.
    """
    return render_template('members/user_profile.html')


@members_bp.route('/users')
@login_required
def users():
    """
    Displays a list of all users.

    Returns:
        The rendered users.html template with a list of users.
    """
    try:
        all_users = User.query.all()
        return render_template('members/users.html', title='Users', users=all_users)
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        flash('An error occurred while retrieving users. Please try again.', 'danger')
        return redirect(url_for('public.index'))


@members_bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    """
    Displays the profile of a specific user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The rendered user_profile.html template with the user's information.
    """
    try:
        user = User.query.get_or_404(user_id)
        return render_template('members/user_profile.html', user=user)
    except Exception as e:
        logger.error(f"Error retrieving user profile for user_id {user_id}: {e}")
        flash('An error occurred while retrieving the user profile. Please try again.', 'danger')
        return redirect(url_for('public.index'))


@members_bp.route('/upload_resume', methods=['GET', 'POST'])
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
    try:
        response = FileHandler.upload(request, user_id)
        logger.info(f"Resume uploaded successfully for user_id {user_id}")
        return response
    except Exception as e:
        logger.error(f"Error uploading resume for user_id {user_id}: {e}")
        return jsonify({"error": "Failed to upload resume"}), 500


@members_bp.route('/analyze_resume', methods=['POST'])
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
    try:
        resume_file = request.files.get('resume_file')
        job_description = request.form.get('job_description')

        if not resume_file or not job_description:
            return jsonify({"error": "Resume file and job description are required"}), 400

        resume_text = ""
        if resume_file.filename.endswith('.docx'):
            document = Document(BytesIO(resume_file.read()))
            for paragraph in document.paragraphs:
                resume_text += paragraph.text + "\n"
        else:
            resume_text = resume_file.read().decode('utf-8')

        if not resume_text.strip():
            return jsonify({"error": "Resume text is required"}), 400

        analysis_result = current_app.ai_service.analyze_resume(resume_text, job_description)
        return jsonify({"analysis_result": analysis_result}), 200
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        return jsonify({"error": "Failed to analyze resume"}), 500


@members_bp.route('/download_sample_resume')
@login_required
def download_sample_resume():
    """
    Serve a sample resume file for download.

    Returns:
        The sample resume file as an attachment.
    """
    try:
        sample_resume_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Brian_resume_1.docx')
        return send_file(sample_resume_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading sample resume: {e}")
        return jsonify({"error": "Failed to download sample resume"}), 500


@login_manager.user_loader
def load_user(user_id):
    """
    Loads the user for Flask-Login.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The User object.
    """
    return User.query.get(int(user_id))
