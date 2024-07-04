"""
Test script for verifying the connection to the Azure SQL Database using pyodbc and SQLAlchemy.

This script attempts to connect to the 'ResuMate' database on 'resumate.database.windows.net'
using the ODBC Driver 17 for SQL Server. If the connection is successful, a success message
is printed. If the connection fails, an error message is printed.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Connection configuration
server = 'BRIANS-DESKTOP\\SQLEXPRESS'
database = 'ResuMate'

# Create connection URL
connection_url = URL.create(
    "mssql+pyodbc",
    host=server,
    database=database,
    query={"driver": "ODBC Driver 17 for SQL Server", "Trusted_Connection": "yes"}
)

# Create engine
engine = create_engine(connection_url)

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Connection successful:", result.fetchone())
except Exception as e:
    print("Connection failed:", e)
