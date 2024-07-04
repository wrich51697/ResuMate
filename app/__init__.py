# __init__.py or your app's initialization module

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()  # Initialize Flask-Migrate


def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.Routes.user_routes import user_bp  # Ensure user_bp is defined in user_routes.py
    from app.Routes.resume_routes import resume_bp  # Ensure resume_bp is defined in resume_routes.py

    app.register_blueprint(user_bp, url_prefix='/auth')
    app.register_blueprint(resume_bp, url_prefix='/resume')

    @app.route('/')
    def home():
        return redirect(url_for('auth.index'))

    return app
