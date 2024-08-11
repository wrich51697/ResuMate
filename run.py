"""
run.py
------------------------------------------------
Author: William Richmond
Created on: 30 June 2024
File name: script.py
Revised: [Add revised date]

Description:
This script initializes the Flask application, creates necessary directories,and sets up the database tables.
 It also runs the Flask development server.

Usage:
    Run this script to start the Flask application and initialize the database.

Example:
    python script.py
"""

import os
import logging
from app import create_app, db_manager  # Import db_manager instead of db

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('script')
handler = logging.FileHandler('script.log')
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
        if not os.path.exists('tests/uploads'):
            os.makedirs('tests/uploads')
            logger.info("Uploads directory created successfully.")

        with app.app_context():
            db_manager.get_db().create_all()  # Use db_manager to create the tables
            logger.info("Database tables created successfully.")

        app.run(debug=True)
    except Exception as e:
        logger.error(f"Error running the application: {e}")
        raise
