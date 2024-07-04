from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import logging

# Setup logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def verify_connection():
    server = 'BRIANS-DESKTOP'  # No instance name needed for default instance
    database = 'ResuMate'

    # Create connection URL
    connection_url = URL.create(
        "mssql+pyodbc",
        username=None,
        password=None,
        host=server,
        port=None,
        database=database,
        query={
            "driver": "ODBC Driver 17 for SQL Server",
            "Trusted_Connection": "yes"
        }
    )

    # Print connection URL
    print(f"Connection URL: {connection_url}")

    # Try connecting to the database
    try:
        engine = create_engine(connection_url)
        connection = engine.connect()
        print("Connection successful!")
        connection.close()
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    verify_connection()
