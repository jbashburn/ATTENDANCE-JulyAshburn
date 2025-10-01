import sqlite3

def create_table_with_user_input(database_name):
    """
    Connects to the specified SQLite database, prompts the user for a 
    table name, and creates a new table with example columns.
    """
    # 1. Get the table name from the user
    table_name = input("Enter the desired name for your new table: ")
    
    if not table_name.strip():
        print("Table name can't be empty. Aborting.")
        return

    # 2. Define the schema for the table
    # This example defines columns suitable for a simple inventory or list.
    table_schema = """
        (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            power_level INTEGER,
            is_mythical BOOLEAN
        )
    """

    # 3. Construct the SQL query
    # The f-string securely places the user's table name into the command.
    sql_query = f"CREATE TABLE {table_name} {table_schema}"

    # 4. Connect to the database and execute the query
    conn = None
    try:
        # Connect to the 'dragon.db' file. It will be created if it doesn't exist.
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Execute the table creation command
        cursor.execute(sql_query)

        # Commit the changes to the database file
        conn.commit()
        print(f"\n✅ Success! Table '{table_name}' has been created in '{database_name}'.")

    except sqlite3.Error as e:
        print(f"\n❌ An error occurred: {e}")
        print("Tip: Ensure the table name doesn't contain spaces or special characters.")
        
    finally:
        # Close the connection
        if conn:
            conn.close()

# ----------------------------------------------------------------------
# --- Main execution block ---

if __name__ == "__main__":
    # Specify the name of your database file
    DB_FILE = "dragon.db"
    
    # Run the function
    create_table_with_user_input(DB_FILE)