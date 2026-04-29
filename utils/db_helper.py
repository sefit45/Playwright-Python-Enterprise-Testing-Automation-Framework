# Import sqlite3 library for database connection
import sqlite3


# Main helper class for database operations
class DBHelper:

    # Constructor runs automatically when object is created
    def __init__(self, db_name):

        # Create connection to SQLite database file
        self.connection = sqlite3.connect(db_name)

        # Create cursor object for executing SQL queries
        self.cursor = self.connection.cursor()

    # Method for executing SELECT query
    def fetch_one(self, query):

        # Execute SQL query
        self.cursor.execute(query)

        # Return first matching row
        return self.cursor.fetchone()

    # Method for executing INSERT / UPDATE / DELETE query
    def execute_query(self, query):

        # Execute SQL query
        self.cursor.execute(query)

        # Save changes permanently
        self.connection.commit()

    # Method for closing database connection
    def close_connection(self):

        # Close DB connection
        self.connection.close()