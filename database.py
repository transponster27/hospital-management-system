#PostgreSQL connection

import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "hospital_db",
    "user": "postgres",
    "password": "Qazq@1212",
    "host": "localhost",
    "port": "5432"
}

#Establish the connection to the database
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

#Create a cursor object to execute SQL queries
def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)