# Flask Application Setup

This document provides instructions for setting up the Flask application for your project.

## Install Flask
First, ensure Flask is installed in your virtual environment.

<procedure title="Install Flask" id="install flask">
    <step>
        <p>Open your terminal or command prompt.</p>
    </step>
    <step>
        <p>Run the following command to install Flask:</p>
        <ul>
            <li><code>pip install flask</code></li>
        </ul>
    </step>
</procedure>

## Create Flask Application Structure

Set up the directory structure for your Flask application. Follow these steps to create the necessary files and directories:

<procedure title="Create Flask Application Structure" id="create-flask-structure">
    <step>
        <p>In the root directory of your project, create the following directories and files:</p>
        <ul>
            <li>
                <code>app/</code> - The main application directory containing the core Flask application files.
                <ul>
                    <li><code>__init__.py</code> - Initializes the Flask application.</li>
                    <li><code>routes.py</code> - Contains the routes for handling different web requests.</li>
                </ul>
            </li>
            <li><code>config.py</code> - Configuration file for the Flask application.</li>
            <li><code>run.py</code> - Script to run the Flask development server.</li>
        </ul>
    </step>
</procedure>

## Initialize the Flask Application

Set up the Flask application by initializing it in the `__init__.py` file.

### Example `__init__.py`:

<procedure title="Initialize Flask Application" id="initialize-flask">
<step>
    <p>Add the following code to your <code>__init__.py</code>:</p>

    from flask import Flask

    def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        # Include our routes
        from . import routes

        return app

</step>
</procedure>

## Define Application Configuration

Configure your Flask application by defining settings in the `config.py` file.

### Example `config.py`:

<procedure title="Define Application Configuration" id="define-config">
<step>
    <p>Add the following code to your: "config.py" file</p>
    
    import os

    class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

</step>
</procedure>

## Define Routes

Create a `routes.py` file in the `app` directory to define the routes for your application.

### Example `routes.py`:

<procedure title="Define Routes" id="define routes">
<step>
    <p>Add the following code to your: "routes.py" file</p>
    
    from flask import current_app as app

    @app.route('/')
    def index():
    return 'Hello, World!'

</step>
</procedure>

## Run the Flask Application

Create a `run.py` file in the root directory to run the Flask application.

### Example `run.py`:

<procedure title="Run Flask Application" id="run-flask">
<step>
    <p>Add the following code to your: "run.py" file:</p>
    
    from app import create_app

    app = create_app()

    if __name__ == '__main__':
    app.run(debug=True)

</step>
</procedure>

## Conclusion

Setting up a Flask application involves installing Flask, creating the application structure, initializing the application, configuring settings, defining routes, and running the application. By following these steps, you can ensure a properly configured and functional Flask application.
