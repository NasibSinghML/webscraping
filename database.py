import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL database connection
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print("Connected to MySQL database")
        return connection

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
print(connect_to_database())