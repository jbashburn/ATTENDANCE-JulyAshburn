import sqlite3
import os

DB_FILE = 'dragon.db'
TABLE_NAME = 'dragons'

def setup_database(conn):
    """Creates a sample table and inserts data if the database is empty."""
    cursor = conn.cursor()
    
    # 1. Create a table if it doesn't exist
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        color TEXT,
        fire_power INTEGER
    );
    """)
    
    # 2. Insert sample data (only if the table is empty)
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ('Ignis', 'Green', 90),
            ('Aether', 'Blue', 75),
            ('Terra', 'Brown', 60)
        ]
        cursor.executemany(f"INSERT INTO {TABLE_NAME} (name, color, fire_power) VALUES (?, ?, ?)", sample_data)
        conn.commit()
        print(f"INFO: Created table '{TABLE_NAME}' and inserted sample data.")


def read_fields_and_data(cursor):
    """Reads the column names and all records from the table."""
    print("--- 1. READING FIELD NAMES (SCHEMA) ---")
    
    # Get column names using PRAGMA
    cursor.execute(f"PRAGMA table_info({TABLE_NAME});")
    column_names = [info[1] for info in cursor.fetchall()]
    print(f"Table: {TABLE_NAME}")
    print(f"Field Names: {column_names}\n")

    print("--- 2. READING ALL DATA ---")
    
    # Read all data
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    rows = cursor.fetchall()
    
    # Print header and data
    header = " | ".join(column_names)
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(map(str, row)))
    print("-" * len(header))
    
    return column_names


def edit_field(conn):
    """Demonstrates updating a field in a record."""
    cursor = conn.cursor()
    
    # Define the update parameters
    target_name = 'Ignis'
    new_color = 'Crimson'
    
    print(f"\n--- 3. EDITING FIELD: Changing color for '{target_name}' ---")

    update_query = f"""
    UPDATE {TABLE_NAME}
    SET color = ?
    WHERE name = ?;
    """

    try:
        # Execute the update
        cursor.execute(update_query, (new_color, target_name))
        
        # Check if any rows were actually updated
        if cursor.rowcount > 0:
            print(f"SUCCESS: Updated {cursor.rowcount} row(s). '{target_name}' color is now '{new_color}'.")
            
            # Commit the changes permanently to the database file
            conn.commit()
        else:
            print(f"WARNING: No row found with name '{target_name}'. No changes committed.")
            
    except sqlite3.Error as e:
        print(f"ERROR: Database update failed: {e}")
        conn.rollback() # Revert any changes if an error occurred


def main():
    """Main function to run the database operations."""
    
    # Use the 'with' statement for automatic connection handling (open/close)
    try:
        with sqlite3.connect(DB_FILE) as conn:
            
            # 0. Setup (Ensures we have a table to work with)
            setup_database(conn)
            
            # Use the cursor for operations
            cursor = conn.cursor()
            
            # 1 & 2. Read the fields and data
            read_fields_and_data(cursor)
            
            # 3. Edit a field
            edit_field(conn)
            
            # Verify the change by reading the data again
            print("\n--- 4. DATA AFTER EDITING ---")
            read_fields_and_data(cursor)
            
    except sqlite3.Error as e:
        print(f"FATAL ERROR: Could not connect to database '{DB_FILE}'. {e}")

if __name__ == "__main__":
    main()