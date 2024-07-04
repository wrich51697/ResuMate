"""
manage.py
------------------------------------------------
Author: Brian Richmond
Created on: 01 July 2024
File name: manage.py
Revised: 14 July 2024

Description:
This script sets up the Flask application, initializing the database and migration tool.
It also provides a command line interface for managing the application.

Usage:
    Run this script to start the Flask application or manage the database.

Example:
    python manage.py runserver
    python manage.py db init
"""

from flask_migrate import Migrate, upgrade, migrate, init
from flask_script import Manager, Command, Option
from app import create_app, db
from app.models import (
    User, Resume, Feedback, Template, ResumeTemplate, Skill, ResumeSkill, JobDescription,
    UserSession, Log, Admin, TemplateCategory, TemplateCategoryMapping, FeedbackTemplate, UploadedFile, AIResult
)

# Create and configure the Flask application
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Script manager
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    """
    Create a shell context that includes the application, database, and models.

    Returns:
        dict: A dictionary of shell context variables.
    """
    return {
        'app': app, 'db': db, 'User': User, 'Resume': Resume, 'Feedback': Feedback, 'Template': Template,
        'ResumeTemplate': ResumeTemplate, 'Skill': Skill, 'ResumeSkill': ResumeSkill, 'JobDescription': JobDescription,
        'UserSession': UserSession, 'Log': Log, 'Admin': Admin, 'TemplateCategory': TemplateCategory,
        'TemplateCategoryMapping': TemplateCategoryMapping, 'FeedbackTemplate': FeedbackTemplate,
        'UploadedFile': UploadedFile, 'AIResult': AIResult
    }


class DbCommand(Command):
    """Perform database migrations."""
    option_list = (
        Option('--command', '-c', dest='command', default='upgrade',
               help='The command to run (init, migrate, upgrade)'),
        Option('--message', '-m', dest='message', default=None, help='The message for the migration')
    )

    def run(self, command, message):
        if command == 'init':
            init(directory='migrations')
        elif command == 'migrate':
            migrate(message=message)
        elif command == 'upgrade':
            upgrade()
        else:
            print(f"Unknown command: {command}")


# Add the custom db command for database migration commands
manager.add_command('db', DbCommand())

if __name__ == '__main__':
    manager.run()
