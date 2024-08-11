"""
upload_utils.py
------------------------------------------------
Author: William Richmond
Created on: 23 July 2024
File name: upload_utils.py
Revised: 23 July 2024

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
import logging
from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename
from app.models import UploadedFile
from app.db_manager import DBManager

# Configure logging
logger = logging.getLogger('upload_utils')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('upload_utils.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

db = DBManager().get_db()


def handle_file_upload():
    """
    Handles the file upload logic and saves the file.

    Returns:
        response (dict): JSON response with the upload status and file ID.
    """
    try:
        logger.info("Handling file upload...")
        if 'file' not in request.files:
            logger.error("No file part in the request")
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        user_id = request.form.get('user_id')
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        uploaded_file = UploadedFile(user_id=user_id, filename=filename, file_path=file_path)
        db.session.add(uploaded_file)
        db.session.commit()

        logger.info(f"File {filename} uploaded successfully by user {user_id}")
        return jsonify({'message': 'File uploaded successfully', 'file_id': uploaded_file.id}), 201
    except Exception as e:
        logger.error(f"Error handling file upload: {e}")
        return jsonify({'error': 'An error occurred during file upload'}), 500
