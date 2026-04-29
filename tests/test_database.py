# Import pytest library for test markers
import pytest

# Import reusable database helper
from utils.db_helper import DBHelper


# DB + Regression test
# This test validates data creation and validation inside database
@pytest.mark.db
@pytest.mark.regression
def test_database_validation():

    # Create DB helper object using local SQLite database file
    db = DBHelper("customers.db")

    # Create customers table if it does not already exist
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    """)

    # Insert sample customer record into table
    db.execute_query("""
        INSERT INTO customers (name, email)
        VALUES ('Sefi', 'sefi@test.com')
    """)

    # Fetch inserted customer from database
    result = db.fetch_one("""
        SELECT name, email
        FROM customers
        WHERE name = 'Sefi'
    """)

    # Validate returned name value
    assert result[0] == "Sefi"

    # Validate returned email value
    assert result[1] == "sefi@test.com"

    # Close DB connection after test ends
    db.close_connection()