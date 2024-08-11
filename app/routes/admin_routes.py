"""
admin_routes.py
------------------------------------------------
Author: William Richmond
Created on: 07 July 2024
File name: admin_routes.py
Revised: [Add revised date]

Description:
This module defines the admin-related routes for the ResuMate application.
It includes routes for managing users, resumes, and viewing analytics.

Usage:
    Import this module and initialize the routes with the given Flask app instance.

Example:
    from admin_routes import admin_bp

    app = Flask(__name__)
    app.register_blueprint(admin_bp, url_prefix='/admin')
"""

import logging
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user  # Added current_user import
from app.models import User
from app.db_manager import DBManager
from app.log import AppLogger

# Initialize logger
app_logger = AppLogger.get_logger()
logger = logging.getLogger('resumate.admin_routes')

admin_bp = Blueprint('admin', __name__, template_folder='app/templates/admin')

# Initialize DBManager
db_manager = DBManager()
db = db_manager.get_db()


@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """
    Renders the admin dashboard.

    Returns:
        The rendered admin_dashboard.html template.
    """
    user_count = User.query.count()
    return render_template('admin/admin_dashboard.html', user_count=user_count)


@admin_bp.route('/users')
@login_required
def admin_users():
    """
    Displays a list of all users for admin.

    Returns:
        The rendered users.html template with a list of users.
    """
    try:
        all_users = User.query.all()
        return render_template('admin/users.html', title='Users', users=all_users)
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        flash('An error occurred while retrieving users. Please try again.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_user_detail(user_id):
    """
    Displays and edits the profile of a specific user. Only the owner can manage admin roles.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The rendered user_detail.html template with the user's information.
    """
    try:
        user = User.query.get_or_404(user_id)
        if request.method == 'POST':
            if current_user.is_owner:
                user.first_name = request.form.get('first_name')
                user.last_name = request.form.get('last_name')
                user.email = request.form.get('email')
                user.is_owner = 'is_owner' in request.form  # Allow owner to set this
                db.session.commit()
                flash('User details updated successfully', 'success')
            else:
                flash('You do not have permission to update this user.', 'danger')
            return redirect(url_for('admin.admin_users'))
        return render_template('admin/user_detail.html', user=user)
    except Exception as e:
        logger.error(f"Error retrieving user profile for user_id {user_id}: {e}")
        flash('An error occurred while retrieving the user profile. Please try again.', 'danger')
        return redirect(url_for('admin.admin_users'))


@admin_bp.route('/logs')
@login_required
def admin_logs():
    """
    Displays system logs for admin.

    Returns:
        The rendered logs.html template with system logs.
    """
    try:
        log_files = ['ai_service.log', 'app.log', 'config.log', 'forms.log', 'resumate.log', 'upload_utils.log',
                     'wsgi.log']
        logs = {}
        for log_file in log_files:
            with open(f'logs/{log_file}', 'r') as file:
                logs[log_file] = file.readlines()
        return render_template('admin/logs.html', title='System Logs', logs=logs)
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        flash('An error occurred while retrieving logs. Please try again.', 'danger')
