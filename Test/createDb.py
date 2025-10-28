# Importing the necessary modules
import sqlite3

# Creating a function to set up the database
def setupDB():
    """
    Create tables for users and their active miners
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.00,
            totalInvested REAL DEFAULT 0.00,
            totalEarnings REAL DEFAULT 0.00
        );
    """)

    # Create the miners table (linked to a user)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS miners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            minerName TEXT NOT NULL,
            cycleDays INTEGER,
            daysRemaining INTEGER,
            projectedReturn REAL DEFAULT 0.00,
            status TEXT
        );
    """)

    conn.commit()
    conn.close()

# 
setupDB()


# Function to insert user data
# def insertUserData(userData):
#     """
#     Insert user and miner data from the userData dictionary
#     """
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Convert numeric strings like "89,500" to float
#     def parse_amount(value):
#         return float(value.replace(",", ""))

#     # Insert into users table
#     cursor.execute("""
#         INSERT INTO users (name, email, balance, totalInvested, totalEarnings)
#         VALUES (?, ?, ?, ?, ?)
#     """, (
#         userData["name"],
#         userData["email"],
#         parse_amount(userData["balance"]),
#         parse_amount(userData["totalInvested"]),
#         parse_amount(userData["totalEarnings"])
#     ))

#     # Get the user ID of the newly inserted user
#     user_id = cursor.lastrowid

#     # Insert into miners table
#     miner = userData["activeMiner"]
#     cursor.execute("""
#         INSERT INTO miners (user_id, name, cycleDays, daysRemaining, projectedReturn, status)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         user_id,
#         miner["name"],
#         miner["cycleDays"],
#         miner["daysRemaining"],
#         parse_amount(miner["projectedReturn"]),
#         miner["status"]
#     ))

#     conn.commit()
#     conn.close()


# # Example user data
# userData = {
#     "name": "Jane Doe",
#     "email": "xyz@gmail.com",
#     "balance": "89,500",
#     "totalInvested": "50,000",
#     "totalEarnings": "39,500",
#     "activeMiner": {
#         "name": "PRO II",
#         "cycleDays": 30,
#         "daysRemaining": 12,
#         "projectedReturn": "17,000",
#         "status": "Mining"
#     }
# }

# # Run setup and insert data
# setupDB()
# insertUserData(userData)
# print("✅ User and miner data inserted successfully!")
