"""
test_db_connection.py
------------------------------------------------
Author: William Richmond
Created on: 09 July 2024
File name: test_db_connection.py
Revised: [Add revised date]

Description:
This module verifies the connection to the SQL Server database using pyodbc and SQLAlchemy.
It attempts to connect to the 'ResuMate' database on 'BRIANS-DESKTOP' using the ODBC Driver 18 for SQL Server.
If the connection is successful, a success message is logged.
If the connection fails, an error message is logged.

Usage:
    Run this module to verify the database connection.

Example:
    python test_db_connection.py
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
import unittest

# Initialize logger
logger = logging.getLogger('resumate.test_db_connection')
logging.basicConfig(level=logging.INFO)

# Connection configuration
server = 'BRIANS-DESKTOP'
database = 'ResuMate'

# Create connection URL
connection_url = URL.create(
    "mssql+pyodbc",
    host=server,
    database=database,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",  # Bypass SSL certificate validation (for testing purposes only)
        "Trusted_Connection": "yes"
    }
)

# Create engine
engine = create_engine(connection_url)


class TestDBConnection(unittest.TestCase):

    def test_connection(self):
        """
        Test the database connection.
        """
        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                first_row = result.fetchone()
                logger.info(f"Connection successful: {first_row}")
                self.assertIsNotNone(first_row)
        except SQLAlchemyError as e:
            logger.error(f"Connection failed: {e}")
            self.fail(f"Connection failed: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.fail(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    unittest.main()
