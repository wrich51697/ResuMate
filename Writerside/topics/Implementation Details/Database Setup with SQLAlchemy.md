# Database Setup with SQLAlchemy

This document provides instructions for setting up a database using SQLAlchemy in your Flask application.

## Install SQLAlchemy
First, ensure SQLAlchemy is installed in your virtual environment.

<procedure title="Install SQLAlchemy" id="install sqlalchemy">
    <step>
        <p>Open your terminal or command prompt.</p>
    </step>
    <step>
        <p>Run the following command to install SQLAlchemy:</p>
        <ul>
            <li><code>pip install flask-sqlalchemy</code></li>
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
    from config import Config</code>
    
    db = SQLAlchemy()

    def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
    db.create_all()

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

        class User(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password_hash = db.Column(db.String(128))

            def __repr__(self):
                return f'<User {self.username}>'
    
</step>
</procedure>

## Configure the Database URI

Configure the database URI in the `config.py` file to point to your database.

### Example `config.py`:

<procedure title="Configure Database URI" id="configure-database-uri">
<step>
    <p>Add or update the following code in your <code>config.py</code>:</p>
    
        import os

        class Config:
            SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
            SQLALCHEMY_TRACK_MODIFICATIONS = False
    
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

        def create_app():
            app = Flask(__name__)
            app.config.from_object(Config)

            db.init_app(app)
            migrate.init_app(app, db)

            with app.app_context():
                db.create_all()

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
