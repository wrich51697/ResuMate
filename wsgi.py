"""
wsgi.py
------------------------------------------------
Author: Brian Richmond
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

app = create_app()

if __name__ == "__main__":
    app.run()
