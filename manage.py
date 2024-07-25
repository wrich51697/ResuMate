"""
manage.py
------------------------------------------------
Author: William Richmond
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

import click
from flask_migrate import Migrate, init as migrate_init, migrate as migrate_migrate, upgrade as migrate_upgrade
from app import create_app
from app.db_manager import db
from app.models import (
    User, Resume, Feedback, Template, ResumeTemplate, Skill, ResumeSkill, JobDescription,
    UserSession, Log, Admin, TemplateCategory, TemplateCategoryMapping, FeedbackTemplate, UploadedFile, AIResult
)

# Create and configure the Flask application
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)


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


@click.group()
def cli():
    pass


@cli.command()
def run():
    """Run the Flask development server."""
    app.run()


@cli.command()
@click.argument('command')
@click.option('--message', '-m', default=None, help='The message for the migration')
def db(command, message):
    """Perform database migrations."""
    with app.app_context():
        if command == 'init':
            migrate_init(directory='migrations')
        elif command == 'migrate':
            migrate_migrate(message=message)
        elif command == 'upgrade':
            migrate_upgrade()
        else:
            click.echo(f"Unknown command: {command}")


if __name__ == '__main__':
    cli()
