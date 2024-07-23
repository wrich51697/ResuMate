"""
upload_utils.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: upload_utils.py
Revised: [Add revised date]

Description:
This module provides utility functions for handling file uploads.

Functions:
    handle_file_upload: Handles the file upload logic and saves the file.

Usage:
    Import the handle_file_upload function and use it in the routes.

Example:
    from app.utils.upload_utils import handle_file_upload
"""

import os
from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename
from app.models import UploadedFile
from app.db_manager import db


def handle_file_upload():
    """
    Handles the file upload logic and saves the file.

    Returns:
        response (dict): JSON response with the upload status and file ID.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    user_id = request.form.get('user_id')
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    uploaded_file = UploadedFile(user_id=user_id, filename=filename, file_path=file_path)
    db.session.add(uploaded_file)
    db.session.commit()

    return jsonify({'message': 'File uploaded successfully', 'file_id': uploaded_file.id}), 201
