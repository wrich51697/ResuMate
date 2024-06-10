from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # Import and initialize routes
    from app.routes import init_routes
    init_routes(app)

    return app
