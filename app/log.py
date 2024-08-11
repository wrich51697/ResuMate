"""
log.py
------------------------------------------------
Author: William Richmond
Created on: 28 July 2024
File name: log.py
Revised:

Description:
This module sets up logging for the ResuMate application.
It configures the logger to log messages to a file with the appropriate format and level.

Classes:
    AppLogger: Handles the creation and configuration of the logger.

Usage:
    Use the AppLogger.get_logger() method to get the configured logger instance.

Example:
    logger = AppLogger.get_logger()
    logger.info('This is an info message')
"""

import logging
import atexit
import os


class AppLogger:
    file_handler = None

    @staticmethod
    def get_logger():
        log_instance = logging.getLogger('resumate')
        if not log_instance.hasHandlers():
            log_instance.setLevel(logging.INFO)

            # Ensure the logs directory exists
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)

            AppLogger.file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
            AppLogger.file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            AppLogger.file_handler.setFormatter(formatter)
            log_instance.addHandler(AppLogger.file_handler)
        return log_instance

    @staticmethod
    def close_logger():
        if AppLogger.file_handler:
            AppLogger.file_handler.close()


# Initialize logger
app_logger = AppLogger.get_logger()

# Make sure to close the logger at application exit
atexit.register(AppLogger.close_logger)
