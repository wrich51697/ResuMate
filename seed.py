"""
seed.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: seed.py
Revised: [Add revised date]

Description:
This script seeds the database with initial data for development and testing purposes.
It includes creating sample users, resumes, and other related data.
"""

import logging
from app import create_app, db_manager  # Import db_manager instead of db
from app.models import User, Resume, Feedback
from flask_bcrypt import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger('seed')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('seed.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = create_app('development')

with app.app_context():
    try:
        # Drop all existing tables and create new ones
        db_manager.get_db().drop_all()
        logger.info("Existing tables dropped.")
        db_manager.get_db().create_all()
        logger.info("Database tables created successfully.")

        # Seed data
        users = [
            User(first_name='John', last_name='Doe', username='johndoe', email='johndoe@example.com',
                 password_hash=generate_password_hash('password').decode('utf-8')),
            User(first_name='Jane', last_name='Smith', username='janesmith', email='janesmith@example.com',
                 password_hash=generate_password_hash('password').decode('utf-8'))
        ]

        resumes = [
            Resume(user_id=1, content='John Doe resume content.'),
            Resume(user_id=2, content='Jane Smith resume content.')
        ]

        feedbacks = [
            Feedback(resume_id=1, content='Great resume, but needs more details in work experience.'),
            Feedback(resume_id=2, content='Consider adding more skills relevant to the job you are applying for.')
        ]

        # Print statements to confirm data is being added
        logger.info("Adding users...")
        db_manager.get_db().session.bulk_save_objects(users)
        logger.info("Users added successfully.")

        logger.info("Adding resumes...")
        db_manager.get_db().session.bulk_save_objects(resumes)
        logger.info("Resumes added successfully.")

        logger.info("Adding feedbacks...")
        db_manager.get_db().session.bulk_save_objects(feedbacks)
        logger.info("Feedbacks added successfully.")

        db_manager.get_db().session.commit()
        logger.info("Database seeded successfully.")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
