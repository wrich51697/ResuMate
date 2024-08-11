# Database Setup with SQLAlchemy

This document provides instructions for setting up a database using SQLAlchemy in your Flask application.

## Install SQLAlchemy and Other Dependencies

First, ensure SQLAlchemy and other required packages are installed in your virtual environment.

<procedure title="Install SQLAlchemy and Other Dependencies" id="install sqlalchemy">
    <step>
        <p>Open your terminal or command prompt.</p>
    </step>
    <step>
        <p>Run the following command to install SQLAlchemy and other dependencies:</p>
        <ul>
            <li><code>pip install flask-sqlalchemy flask-migrate flask-bcrypt flask-login</code></li>
        </ul>
    </step>
</procedure>

## Initialize SQLAlchemy in Flask

Initialize SQLAlchemy in your Flask application.

### Update `__init__.py` in the `app` directory:

<procedure title="Initialize SQLAlchemy in Flask" id="initialize-sqlalchemy">
<step>
    <p>Add the following code to your <code>__init__.py</code>:</p>
    <code>
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_bcrypt import Bcrypt
    from flask_login import LoginManager
    from config import Config</code>

    db = SQLAlchemy()
    migrate = Migrate()
    bcrypt = Bcrypt()
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    def create_app(config_class=Config):
        app = Flask(__name__, template_folder='../templates')
        app.config.from_object(config_class)

        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        login_manager.init_app(app)

        from app import routes  # Import routes module
        routes.init_routes(app)  # Initialize routes

        from app.models import User  # Import User model for login management

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        return app
</step>
</procedure>

## Create Database Models

Define your database models using SQLAlchemy. Create a `models.py` file in the `app` directory and add your models.

### Example `models.py`:

<procedure title="Create Database Models" id="create database models">
<step>
    <p>Add the following code to your <code>models.py</code>:</p>

        from app import db
        from flask_login import UserMixin

        class User(db.Model, UserMixin):
            id = db.Column(db.Integer, primary_key=True)
            first_name = db.Column(db.String(64), nullable=False)
            last_name = db.Column(db.String(64), nullable=False)
            username = db.Column(db.String(64), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password_hash = db.Column(db.String(128))
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
            updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

            def __repr__(self):
                return f'<User {self.username}>'
        
        class Resume(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            content = db.Column(db.Text)
            uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
            updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

        class Feedback(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
            content = db.Column(db.Text)
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

        class Template(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(128))
            file_path = db.Column(db.String(256))
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
            updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

        class ResumeTemplate(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
            template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
            applied_at = db.Column(db.DateTime, default=db.func.current_timestamp())

        class Skill(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(128))

        class ResumeSkill(db.Model):
            resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), primary_key=True)
            skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)

        class JobDescription(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(128))
            description = db.Column(db.Text)
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
            updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

        class UserSession(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            session_token = db.Column(db.String(128), unique=True)
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
            expires_at = db.Column(db.DateTime)

        class Log(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            action = db.Column(db.String(128))
            timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

        class Admin(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password_hash = db.Column(db.String(128))
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
            updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

        class TemplateCategory(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(128))
            description = db.Column(db.Text)

        class TemplateCategoryMapping(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
            category_id = db.Column(db.Integer, db.ForeignKey('template_category.id'))

        class FeedbackTemplate(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(128))
            content = db.Column(db.Text)
            created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
</step>
</procedure>

## Configure the Database URI

Configure the database URI in the `config.py` file to point to your database.

### Example `config.py`:

<procedure title="Configure Database URI" id="configure-database-uri">
<step>
    <p>Add or update the following code in your <code>config.py</code>:</p>

        import os
        from sqlalchemy.engine import URL

        class Config:
            SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
            database_url = URL.create(
                "mssql+pyodbc",
                username="",
                password="",
                host="BRIANS-DESKTOP\\SQLEXPRESS",
                database="ResuMate",
                query={"driver": "ODBC Driver 17 for SQL Server", "trusted_connection": "yes"}
            )
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or str(database_url)
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SQLALCHEMY_ECHO = True

</step>
</procedure>

## Migrate the Database

Use Flask-Migrate to handle database migrations.

### Install Flask-Migrate

<procedure title="Install Flask-Migrate" id="install flask migrate">
<step>
    <p>Run the following command to install Flask-Migrate:</p>

        pip install flask-migrate
</step>
</procedure>

### Initialize Flask-Migrate

<procedure title="Initialize Flask-Migrate" id="initialize flask migrate">
<step>
    <p>Add the following code to your <code>__init__.py</code>:</p>

        from flask_migrate import Migrate

        migrate = Migrate()

        def create_app(config_class=Config):
            app = Flask(__name__, template_folder='../templates')
            app.config.from_object(config_class)

            db.init_app(app)
            migrate.init_app(app, db)
            bcrypt.init_app(app)
            login_manager.init_app(app)

            from app import routes  # Import routes module
            routes.init_routes(app)  # Initialize routes

            from app.models import User  # Import User model for login management

            @login_manager.user_loader
            def load_user(user_id):
                return User.query.get(int(user_id))

            return app

</step>
</procedure>

### Create and Apply Migrations

<procedure title="Create and Apply Migrations" id="create-apply-migrations">
<step>
    <p>Run the following commands to create and apply database migrations:</p>
    <ul>
        <li><code>flask db init</code> (only run this once to initialize migrations)</li>
        <li><code>flask db migrate -m "Initial migration"</code></li>
        <li><code>flask db upgrade</code></li>
    </ul>
</step>
</procedure>

## Conclusion

Setting up SQLAlchemy with Flask allows for a powerful and flexible database solution for your application. By following these steps, you can ensure a properly configured database setup and manage migrations effectively.
