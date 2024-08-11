# Flask Application Setup

This document provides instructions for setting up a Flask application with essential extensions.

## Setting Up the Flask Application

First, ensure you have set up the virtual environment as described in the Environment Setup section.

<procedure title="Set Up Flask Application" id="setup-flask-application">
    <step>
        <p>Install Flask by running the following command:</p>
        <pre>
        pip install Flask
        </pre>
    </step>
</procedure>

## Install Dependencies {id="install-dependencies_1"}

Ensure all necessary packages are installed in your virtual environment.

<procedure title="Install Dependencies" id="install-dependencies">
    <step>
        <p>Open your terminal or command prompt.</p>
    </step>
    <step>
        <p>Run the following command to install the required packages:</p>
        <ul>
            <li><code>pip install flask flask-sqlalchemy flask-migrate flask-bcrypt flask-login</code></li>
        </ul>
    </step>
</procedure>

## Create the Application Structure

Create the necessary directories and files for your Flask application.

<procedure title="Create Application Structure" id="create-application-structure">
    <step>
        <p>In your project root directory, create the following structure:</p>
        <pre>
       project/
        │
        ├── app/
        │ ├── init.py
        │ ├── models.py
        │ ├── routes.py
        │ ├── forms.py
        │ └── templates/
        │ ├── base.html
        │ ├── index.html
        │ ├── create_user.html
        │ ├── edit_user.html
        │ ├── list_users.html
        │ ├── login.html
        │ └── user_detail.html
        │
        ├── migrations/
        │
        ├── static/
        │ └── style.css
        │
        ├── instance/
        │ └── resumate.db
        │
        ├── .venv/
        │
        ├── config.py
        │
        ├── wsgi.py
        │
        └── requirements.txt
        </pre>
    </step>
</procedure>

## Initialize Flask Application {id="initialize-flask-application_1"}

Initialize the Flask application in `__init__.py`.

<procedure title="Initialize Flask Application" id="initialize-flask-application">
    <step>
        <p>Add the following code to your <code>app/__init__.py</code>:</p>
        <pre>
        from flask import Flask
        app = Flask(__name__)
        from app import routes
        </pre>
    </step>
</procedure>

## Update `__init__.py` in the `app` directory:

<procedure title="Initialize Flask Application" id="initialize-flask">
<step>
    <p>Add the following code to your <code>__init__.py</code>:</p>

    ```python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_bcrypt import Bcrypt
    from flask_login import LoginManager
    from config import Config

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
    ```
</step>
</procedure>

## Create Routes {id="create-routes_1"}

Define your application routes in `routes.py`.

<procedure title="Create Routes" id="create-routes">
    <step>

    ```python
    from flask import render_template, url_for, flash, redirect, request
    from app import app, db, bcrypt
    from app.forms import RegistrationForm, LoginForm
    from app.models import User
    from flask_login import login_user, current_user, logout_user, login_required

    def init_routes(app):
        @app.route("/")
        @app.route("/index")
        def index():
            return render_template('index.html', title='Home')

        @app.route("/register", methods=['GET', 'POST'])
        def register():
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            form = RegistrationForm()
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash('Your account has been created!', 'success')
                return redirect(url_for('login'))
            return render_template('register.html', title='Register', form=form)

        @app.route("/login", methods=['GET', 'POST'])
        def login():
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            form = LoginForm()
            if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                    login_user(user, remember=form.remember.data)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('index'))
                else:
                    flash('Login unsuccessful. Please check email and password', 'danger')
            return render_template('login.html', title='Login', form=form)

        @app.route("/logout")
        def logout():
            logout_user()
            return redirect(url_for('index'))

        @app.route("/users")
        @login_required
        def users():
            users = User.query.all()
            return render_template('users.html', users=users)
    ```
</step>
</procedure>
## Run the Application

Run the Flask application using `run.py`.

<procedure title="Run Application" id="run-application">
    <step>
        <p>Create a `run.py` file with the following code:</p>
        <pre>
        from app import app
        if __name__ == '__main__':
            app.run(debug=True)
        </pre>
    </step>
    <step>
        <p>Run the application:</p>
        <pre>
        python run.py
        </pre>
    </step>
</procedure>

## Conclusion

Setting up a Flask application involves creating the application structure,
initializing the application, defining routes, and running the application.
By following these steps, you will have a basic Flask application up and running.
