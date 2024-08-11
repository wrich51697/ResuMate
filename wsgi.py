"""
wsgi.py
------------------------------------------------
Author: William Richmond
Created on: 01 July 2024
File name: wsgi.py
Revised:

Description:
This module serves as the entry point for the ResuMate application.
It creates the Flask app instance and runs the application.

Usage:
    Run this module to start the Flask application.

Example:
    python wsgi.py
"""

from app import create_app
import logging

# Setup logging
logger = logging.getLogger('wsgi')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/wsgi.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    app = create_app()
except Exception as e:
    logger.error(f"Error creating the Flask application: {e}")
    raise

if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        logger.error(f"Error running the application: {e}")
        raise
