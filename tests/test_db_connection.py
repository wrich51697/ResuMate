"""
Test script for verifying the connection to the SQL Server database using pyodbc and SQLAlchemy.

This script attempts to connect to the 'ResuMate' database on 'BRIANS-DESKTOP'
using the ODBC Driver 18 for SQL Server. If the connection is successful, a success message
is printed. If the connection fails, an error message is printed.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

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

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful: ", result.fetchone())
except SQLAlchemyError as e:
    print("Connection failed: ", e)
except Exception as e:
    print("An unexpected error occurred: ", e)
