import psycopg2
import json
from datetime import datetime

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Database configuration
db_config = config['database']

def log_sound_event(sound_level, timestamp):
    """
    Logs a sound event to the remote SQL database.
    
    :param connection: A connection to the database.
    :param sound_level: The sound level that triggered the event.
    :param timestamp: The timestamp of when the event occurred.
    """
    connection= connect_to_database()
    cursor = connection.cursor()
    query = 'INSERT INTO babynoise.sound_events (sound_level, event_time) VALUES (%s, %s)'
    cursor.execute(query, (sound_level, timestamp))
    connection.commit()
    cursor.close()
    close_database_connection(connection)

def connect_to_database():
    """
    Establishes a connection to the remote SQL database and validates its existence.
    If the database does not exist, it attempts to create it.
    
    :return: A connection object to the database.
    """
    try:
        # Attempt to connect to the database
        connection = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            dbname=db_config['dbname']
        )
        return connection
    except psycopg2.Error as err:
        print(err)


def create_database_structure():
    """
    Checks if the database and its structure exist, and creates them if they do not.
    :return: A connection object to the database, or None if failed.
    """
    # Step 1: Confirm connection to database
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            dbname='postgres'  # Default database
        )
        connection.autocommit = True
        print(" - connected to postgres server")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_config['dbname']}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_config['dbname']}")
        cursor.close()
        print(" - created database")
    except Exception as e:
        print(f"Failed to create database: {e}")
        return False
    
    # Step 2: Confirm existance of schema "BABYNOISE"
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE SCHEMA IF NOT EXISTS babynoise;")
        cursor.close()
        print(" - created schema")
    except Exception as e:
        print(f"Failed to create schema: {e}")
        return False

    # Step 3: Confirm existance of table "sound_events"
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS babynoise.sound_events (id SERIAL PRIMARY KEY, sound_level INT, event_time TIMESTAMP);")
        cursor.close()
        print(" - created table")
    except Exception as e:
        print(f"Failed to create table: {e}")
        return False
    
    connection.commit()
    close_database_connection(connection)
    return True
    
        
    
def close_database_connection(connection):
    """
    Closes the connection to the database.
    
    :param connection: The database connection to close.
    """
    if connection:
        connection.close()

# # Example usage
# if __name__ == "__main__":
#     # Connect to the database
#     db_conn = connect_to_database()
#     if db_conn:
#         # Log a test sound event
#         log_sound_event(db_conn, 75, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#         # Close the database connection
#         close_database_connection(db_conn)