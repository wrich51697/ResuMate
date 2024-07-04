"""
This module defines the database models for the ResuMate application.
It includes models for users, resumes, feedback, templates, skills, job descriptions, sessions, logs, and admins.
Each model includes fields, relationships, and methods for interacting with the database.
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): Primary key.
        first_name (str): User's first name.
        last_name (str): User's last name.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def set_password(self, password):
        """
        Set the user's password by hashing it.

        Args:
            password (str): The user's password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


class Resume(db.Model):
    """
    Represents a résumé in the application.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user who uploaded the résumé.
        content (str): Content of the résumé.
        uploaded_at (datetime): Timestamp when the résumé was uploaded.
        updated_at (datetime): Timestamp when the résumé was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Feedback(db.Model):
    """
    Represents feedback on a résumé.

    Attributes:
        id (int): Primary key.
        resume_id (int): Foreign key to the résumé the feedback is about.
        content (str): Content of the feedback.
        created_at (datetime): Timestamp when the feedback was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Template(db.Model):
    """
    Represents a template for resumes or feedback.

    Attributes:
        id (int): Primary key.
        name (str): Name of the template.
        file_path (str): Path to the template file.
        created_at (datetime): Timestamp when the template was created.
        updated_at (datetime): Timestamp when the template was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    file_path = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class ResumeTemplate(db.Model):
    """
    Represents a mapping between a résumé and a template.

    Attributes:
        id (int): Primary key.
        resume_id (int): Foreign key to the résumé.
        template_id (int): Foreign key to the template.
        applied_at (datetime): Timestamp when the template was applied to the résumé.
    """
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    applied_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Skill(db.Model):
    """
    Represents a skill that can be associated with a résumé.

    Attributes:
        id (int): Primary key.
        name (str): Name of the skill.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class ResumeSkill(db.Model):
    """
    Represents a mapping between a résumé and a skill.

    Attributes:
        resume_id (int): Foreign key to the résumé.
        skill_id (int): Foreign key to the skill.
    """
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)


class JobDescription(db.Model):
    """
    Represents a job description.

    Attributes:
        id (int): Primary key.
        title (str): Title of the job.
        description (str): Description of the job.
        created_at (datetime): Timestamp when the job description was created.
        updated_at (datetime): Timestamp when the job description was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class UserSession(db.Model):
    """
    Represents a user session.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user.
        session_token (str): Unique session token.
        created_at (datetime): Timestamp when the session was created.
        expires_at (datetime): Timestamp when the session expires.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_token = db.Column(db.String(128), unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime)


class Log(db.Model):
    """
    Represents a log entry for user actions.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to the user.
        action (str): Description of the action.
        timestamp (datetime): Timestamp when the action was logged.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class Admin(db.Model):
    """
    Represents an admin user in the application.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password.
        created_at (datetime): Timestamp when the admin was created.
        updated_at (datetime): Timestamp when the admin was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class TemplateCategory(db.Model):
    """
    Represents a category for templates.

    Attributes:
        id (int): Primary key.
        name (str): Name of the category.
        description (str): Description of the category.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)


class TemplateCategoryMapping(db.Model):
    """
    Represents a mapping between a template and a category.

    Attributes:
        id (int): Primary key.
        template_id (int): Foreign key to the template.
        category_id (int): Foreign key to the category.
    """
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('template_category.id'))


class FeedbackTemplate(db.Model):
    """
    Represents a feedback template.

    Attributes:
        id (int): Primary key.
        title (str): Title of the feedback template.
        content (str): Content of the feedback template.
        created_at (datetime): Timestamp when the feedback template was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
