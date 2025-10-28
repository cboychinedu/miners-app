# Importing the necessary moduels 
import sqlite3 

# Creating a function to setup the database 
def setupDB(): 
    """
        Create an empty table for the user 
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor() 

    # Set an sql query 
    query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """

    # Execute the commands 
    cursor.execute(query) 

    # Commit the commands 
    conn.commit()
    conn.close() 


# Running the program 
setupDB(); 