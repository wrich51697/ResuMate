"""
forms.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: forms.py
Revised: [Add revised date]

Description:
This module defines form classes for user registration and login using Flask-WTF.
It includes custom validation functions for username and email uniqueness.

Forms:
    RegistrationForm: Handles user registration.
    LoginForm: Handles user login.

Usage:
    Import the forms and use them in the routes for user registration and login.

Example:
    from forms import RegistrationForm, LoginForm
"""

import logging
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger('forms')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('forms.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def validate_username(form, field):
    """
    Validate that the username is unique.

    Args:
        form (FlaskForm): The form instance.
        field (Field): The field to validate.

    Raises:
        ValidationError: If the username is already taken.
    """
    try:
        user = User.query.filter_by(username=field.data).first()
        if user:
            logger.info(f"Validation error: Username '{field.data}' is already taken.")
            raise ValidationError('That username is taken. Please choose a different one.')
    except SQLAlchemyError as e:
        logger.error(f"Database error during username validation: {e}")
        raise ValidationError('Error accessing the database. Please try again later.')


def validate_email(form, field):
    """
    Validate that the email is unique.

    Args:
        form (FlaskForm): The form instance.
        field (Field): The field to validate.

    Raises:
        ValidationError: If the email is already taken.
    """
    try:
        user = User.query.filter_by(email=field.data).first()
        if user:
            logger.info(f"Validation error: Email '{field.data}' is already taken.")
            raise ValidationError('That email is taken. Please choose a different one.')
    except SQLAlchemyError as e:
        logger.error(f"Database error during email validation: {e}")
        raise ValidationError('Error accessing the database. Please try again later.')


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Fields:
        first_name (StringField): User's first name.
        last_name (StringField): User's last name.
        username (StringField): Desired username.
        email (StringField): User's email address.
        password (PasswordField): User's password.
        confirm_password (PasswordField): Confirmation of the user's password.
        submit (SubmitField): Submit button.
    """
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20), validate_username])
    email = StringField('Email', validators=[DataRequired(), Email(), validate_email])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    Form for user login.

    Fields:
        email (StringField): User's email address.
        password (PasswordField): User's password.
        remember (BooleanField): Option to remember the user.
        submit (SubmitField): Submit button.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
