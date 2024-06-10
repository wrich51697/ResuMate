# test_connection.py

import pyodbc

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=BRIANS-DESKTOP\\SQLEXPRESS;'
    'DATABASE=resumate;'
    'Trusted_Connection=yes;'
)
try:
    with pyodbc.connect(conn_str) as conn:
        print("Connection successful!")
except pyodbc.Error as ex:
    print("Connection failed:", ex)
