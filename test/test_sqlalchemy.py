"""
Test script for verifying the creation of a table in the SQL Server database using SQLAlchemy.

This script connects to the 'ResuMate' database on 'BRIANS-DESKTOP'
using the ODBC Driver 17 for SQL Server, creates a metadata object, defines a test table,
and creates the table in the database.
If the table creation is successful, a success message is printed.
This script is integrated with the unittest framework for comprehensive testing.
"""

import unittest
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


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
        # Database connection URI for SQLAlchemy
        connection_url = URL.create(
            "mssql+pyodbc",
            host='BRIANS-DESKTOP',
            database='ResuMate',
            query={"driver": "ODBC Driver 17 for SQL Server", "Trusted_Connection": "yes"}
        )

        try:
            self.engine = create_engine(connection_url, echo=True)
            self.metadata = MetaData()

            # Define a test table
            self.test_table = Table('test', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', String))

            # Create all tables in the metadata
            self.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            self.fail(f"Error setting up the database: {e}")

    def tearDown(self):
        """
        Tear down the test context.

        This method is called after each test.
        It drops all tables defined in the metadata
        from the database.
        """
        try:
            self.metadata.drop_all(self.engine)
        except SQLAlchemyError as e:
            self.fail(f"Error tearing down the database: {e}")

    def test_table_creation(self):
        """
        Test the creation of the test table.

        This test verifies that the test table is created successfully in the database.
        It checks the existence of the table in the metadata and ensures the database
        connection is operational.
        """
        with self.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            self.assertIsNotNone(result)
            self.assertIn('test', self.metadata.tables)
            print("Table created successfully!")


if __name__ == '__main__':
    unittest.main()
