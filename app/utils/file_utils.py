"""
file_utils.py
------------------------------------------------
Author: William Richmond
Created on: 08 July 2024
File name: file_utils.py
Revised: [Add revised date]

Description:
This module provides utility functions for handling file operations.

Functions:
    save_file: Saves an uploaded file to the specified directory.

Usage:
    Import this module and use the save_file function to handle file saving operations.

Example:
    file_path, filename = save_file(file, upload_folder)
"""

import os
import logging
from werkzeug.utils import secure_filename

# Configure logging
logger = logging.getLogger('file_utils')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('file_utils.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def save_file(file, upload_folder):
    """
    Saves an uploaded file to the specified directory.

    Args:
        file (FileStorage): The file to be saved.
        upload_folder (str): The directory to save the file.

    Returns:
        tuple: The file path and the secure filename.
    """
    logger.info(f"Saving file {file.filename} to {upload_folder}...")
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    logger.info(f"File {filename} saved successfully to {file_path}")
    return file_path, filename
