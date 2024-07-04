"""
This script sets up the Flask application, initializing the database and migration tool.
It also provides a command line interface for managing the application.
"""

from app import create_app, db
from app.models import User
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    Create a shell context that includes the application, database, and models.

    Returns:
        dict: A dictionary of shell context variables.
    """
    return {'app': app, 'db': db, 'User': User}


if __name__ == '__main__':
    app.run()
