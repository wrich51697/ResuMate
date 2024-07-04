"""
Test script for verifying the creation of a table in the SQL Server database using SQLAlchemy.

This script connects to the 'resumate' database on 'BRIANS-DESKTOP\\SQLEXPRESS'
using the ODBC Driver 17 for SQL Server, creates a metadata object, defines a test table,
and creates the table in the database. If the table creation is successful, a success message
is printed.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# Database connection URI for SQLAlchemy
DATABASE_URI = ('mssql+pyodbc://BRIANS-DESKTOP\\SQLEXPRESS/resumate?driver=ODBC+Driver+17+for+SQL+Server'
                ';trusted_connection=yes')

# Create an engine instance
engine = create_engine(DATABASE_URI, echo=True)

# Create a metadata instance
metadata = MetaData()

# Define a test table
test_table = Table('test', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String))

# Create all tables in the metadata
metadata.create_all(engine)

print("Table created successfully!")
