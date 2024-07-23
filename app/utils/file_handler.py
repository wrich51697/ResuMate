"""
file_handler.py
------------------------------------------------
Author: Brian Richmond
Created on: 08 July 2024
File name: file_handler.py
Revised: [Add revised date]

Description:
This module provides file handling functionality for uploading and managing files.

Classes:
    FileHandler: A class to handle file uploads and save them to the database.

Usage:
    Import this module and use the FileHandler class to handle file uploads.

Example:
    from app.utils.file_handler import FileHandler

    handler = FileHandler()
    response = handler.upload(request)
"""

import os
from flask import flash, redirect, url_for, jsonify, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.db_manager import db
from app.models import Resume, UploadedFile


class FileHandler:
    """
    A class to handle file uploads and save them to the database.
    """

    @staticmethod
    def upload(request, user_id=None):
        """
        Save an uploaded file and store its information in the database.

        Args:
            request (Request): The Flask request object containing the file.
            user_id (int, optional): The ID of the user uploading the file.
            Defaults to None.

        Returns:
            tuple: JSON response with the upload status and file ID, and the status code.
        """
        if 'resume' not in request.files and 'file' not in request.files:
            flash('No file part', 'danger')
            return jsonify({'message': 'No file part'}), 400

        file = request.files.get('resume') or request.files.get('file')
        if file.filename == '':
            flash('No selected file', 'danger')
            return jsonify({'message': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if user_id is None:
            user_id = current_user.id

        # Save the file information to the database
        uploaded_file = UploadedFile(user_id=user_id, filename=filename, file_path=file_path)
        db.session.add(uploaded_file)
        db.session.commit()

        flash('File successfully uploaded', 'success')
        return jsonify({'message': 'File uploaded successfully', 'file_id': uploaded_file.id}), 201

    @staticmethod
    def upload_resume(request):
        """
        Handles the specific upload of resume files.

        Args:
            request (Request): The Flask request object containing the resume file.

        Returns:
            tuple: JSON response with the upload status and redirect if successful.
        """
        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return jsonify({'message': 'No file part'}), 400

        file = request.files['resume']
        if file.filename == '':
            flash('No selected file', 'danger')
            return jsonify({'message': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(os.getcwd(), 'app/static/uploads', filename)
        file.save(file_path)

        new_resume = Resume(user_id=current_user.id, content=file.read())
        db.session.add(new_resume)
        db.session.commit()

        flash('File successfully uploaded', 'success')
        return redirect(url_for('auth.index'))
