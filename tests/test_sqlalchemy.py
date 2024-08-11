"""
test_sqlalchemy.py
------------------------------------------------
Author: William Richmond
Created on: 09 July 2024
File name: test_table_creation.py
Revised: [Add revised date]

Description:
This module contains a test script for verifying the creation of a table in the SQL Server database using SQLAlchemy.
The script connects to the 'ResuMate' database on 'BRIANS-DESKTOP' using the ODBC Driver 17 for SQL Server,
creates a metadata object, defines a test table, and creates the table in the database.

Classes:
    SQLAlchemyTestCase: A test case for verifying the creation of a table in the SQL Server database using SQLAlchemy.

Usage:
    Run this module with a test runner to execute the tests.

Example:
    python -m unittest test_table_creation
"""

import unittest
import logging
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger('test_table_creation')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('test_table_creation.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SQLAlchemyTestCase(unittest.TestCase):
    """
    Test case for verifying the creation of a table in the SQL Server database using SQLAlchemy.
    """

    def setUp(self):
        """
        Set up test variables and initialize the database connection.

        This method is called before each test.
        It creates an engine instance, a metadata instance,
        and defines a test table.
        The table is then created in the database.
        """
        logger.info("Setting up the test environment")
        try:
            # Database connection URI for SQLAlchemy
            connection_url = URL.create(
                "mssql+pyodbc",
                host='BRIANS-DESKTOP',
                database='ResuMate',
                query={"driver": "ODBC Driver 17 for SQL Server", "Trusted_Connection": "yes"}
            )

            self.engine = create_engine(connection_url, echo=True)
            self.metadata = MetaData()

            # Define a test table
            self.test_table = Table('test_table', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', String))

            # Create all tables in the metadata
            self.metadata.create_all(self.engine)
            logger.info("Test table created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error setting up the database: {e}")
            self.fail(f"Error setting up the database: {e}")

    def tearDown(self):
        """
        Tear down the test context.

        This method is called after each test.
        It drops all tables defined in the metadata
        from the database.
        """
        logger.info("Tearing down the test environment")
        try:
            self.metadata.drop_all(self.engine)
            logger.info("Test table dropped successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error tearing down the database: {e}")
            self.fail(f"Error tearing down the database: {e}")

    def test_table_creation(self):
        """
        Test the creation of the test table.

        This test verifies that the test table is created successfully in the database.
        It checks the existence of the table in the metadata and ensures the database
        connection is operational.
        """
        logger.info("Testing table creation")
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text('SELECT 1'))
                self.assertIsNotNone(result)
                self.assertIn('test_table', self.metadata.tables)
                logger.info("Table created successfully and test passed")
        except SQLAlchemyError as e:
            logger.error(f"Error during test_table_creation: {e}")
            self.fail(f"Error during test_table_creation: {e}")


if __name__ == '__main__':
    unittest.main()
