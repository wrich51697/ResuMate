"""
models.py
------------------------------------------------
Author: Brian Richmond
Created on: 07 July 2024
File name: models.py
Revised: [Add revised date]

Description:
This module defines the database models for the ResuMate application.
It includes models for users, resumes, feedback, template, skills, job descriptions, sessions, logs, and admins.
Each model includes fields, relationships, and methods for interacting with the database.

Classes:
    User: Represents a user in the application.
    Resume: Represents a résumé in the application.
    Feedback: Represents feedback on a résumé.
    Template: Represents a template for resumes or feedback.
    ResumeTemplate: Represents a mapping between a résumé and a template.
    Skill: Represents a skill that can be associated with a résumé.
    ResumeSkill: Represents a mapping between a résumé and a skill.
    JobDescription: Represents a job description.
    UserSession: Represents a user session.
    Log: Represents a log entry for user actions.
    Admin: Represents an admin user in the application.
    TemplateCategory: Represents a category for template.
    TemplateCategoryMapping: Represents a mapping between a template and a category.
    FeedbackTemplate: Represents a feedback template.
    UploadedFile: Represents a file uploaded by a user.
    AIResult: Represents the AI processing result of an uploaded file.

Usage:
    Import the models module and use the classes to interact with the database.

Example:
    from app.models import User
"""

from hashlib import md5
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.db_manager import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Specify the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    resumes = db.relationship('Resume', back_populates='user')
    sessions = db.relationship('UserSession', back_populates='user')
    logs = db.relationship('Log', back_populates='user')
    uploads = db.relationship('UploadedFile', back_populates='user')

    def __init__(self, first_name, last_name, username, email, password_hash, is_active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return f'<User {self.username}>'


class Resume(db.Model):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user = db.relationship('User', back_populates='resumes')
    feedback = db.relationship('Feedback', back_populates='resume', lazy='dynamic')
    templates = db.relationship('ResumeTemplate', back_populates='resume', lazy='dynamic')
    skills = db.relationship('ResumeSkill', back_populates='resume', lazy='dynamic')

    def __repr__(self):
        return f'<Resume {self.id} by User {self.user_id}>'


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    resume = db.relationship('Resume', back_populates='feedback')

    def __repr__(self):
        return f'<Feedback {self.id} for Resume {self.resume_id}>'


class Template(db.Model):
    __tablename__ = 'template'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    resumes = db.relationship('ResumeTemplate', back_populates='template', lazy='dynamic')
    categories = db.relationship('TemplateCategoryMapping', back_populates='template', lazy='dynamic')

    def __repr__(self):
        return f'<Template {self.name}>'


class ResumeTemplate(db.Model):
    __tablename__ = 'resume_template'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    resume = db.relationship('Resume', back_populates='templates')
    template = db.relationship('Template', back_populates='resumes')

    def __repr__(self):
        return f'<ResumeTemplate {self.id}>'


class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    resumes = db.relationship('ResumeSkill', back_populates='skill', lazy='dynamic')

    def __repr__(self):
        return f'<Skill {self.name}>'


class ResumeSkill(db.Model):
    __tablename__ = 'resume_skill'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    resume = db.relationship('Resume', back_populates='skills')
    skill = db.relationship('Skill', back_populates='resumes')

    def __repr__(self):
        return f'<ResumeSkill {self.id}>'


class JobDescription(db.Model):
    __tablename__ = 'job_description'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<JobDescription {self.title}>'


class UserSession(db.Model):
    __tablename__ = 'user_session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_token = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', back_populates='sessions')

    def __repr__(self):
        return f'<UserSession {self.id}>'


class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', back_populates='logs')

    def __repr__(self):
        return f'<Log {self.id}>'


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class TemplateCategory(db.Model):
    __tablename__ = 'template_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128))
    template = db.relationship('TemplateCategoryMapping', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f'<TemplateCategory {self.name}>'


class TemplateCategoryMapping(db.Model):
    __tablename__ = 'template_category_mapping'

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('template_category.id'), nullable=False)
    template = db.relationship('Template', back_populates='categories')
    category = db.relationship('TemplateCategory', back_populates='template')

    def __repr__(self):
        return f'<TemplateCategoryMapping {self.id}>'


class FeedbackTemplate(db.Model):
    __tablename__ = 'feedback_template'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<FeedbackTemplate {self.title}>'


class UploadedFile(db.Model):
    __tablename__ = 'uploaded_file'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    user = db.relationship('User', back_populates='uploads')
    ai_results = db.relationship('AIResult', back_populates='file', lazy='dynamic')

    def __repr__(self):
        return f'<UploadedFile {self.filename}>'


class AIResult(db.Model):
    __tablename__ = 'ai_result'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('uploaded_file.id'), nullable=False)
    result_data = db.Column(db.Text, nullable=False)
    file = db.relationship('UploadedFile', back_populates='ai_results')

    def __repr__(self):
        return f'<AIResult {self.id}>'
