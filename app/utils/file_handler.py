"""
file_handler.py
------------------------------------------------
Author: Brian Richmond
Created on: 08 July 2024
File name: file_handler.py
Revised: 08 July 2024

Description:
This module provides file handling functionality for uploading and managing files.

Usage:
    Import this module and use the FileHandler class to handle file uploads.

Example:
    from app.utils.file_handler import FileHandler

    handler = FileHandler()
    handler.upload(request)
"""

import os
from flask import flash, redirect, url_for, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.db_manager import db
from app.models import Resume


class FileHandler:
    @staticmethod
    def upload(request):
        if 'resume' not in request.files:
            flash('No file part', 'danger')
            return jsonify({'message': 'No file part'}), 400
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file', 'danger')
            return jsonify({'message': 'No selected file'}), 400
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(os.getcwd(), 'app/static/uploads', filename)
            file.save(file_path)
            new_resume = Resume(user_id=current_user.id, content=file.read())
            db.session.add(new_resume)
            db.session.commit()
            flash('File successfully uploaded', 'success')
            return redirect(url_for('auth.index'))
        return jsonify({'message': 'File not uploaded'}), 400
