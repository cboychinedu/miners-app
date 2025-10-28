# Importing the necessary modules 
import os 
import sqlite3 

# Defining the path to the database file 
databasePath = os.path.join(os.path.dirname(__file__), 'database.db')

# Creating a class to manage the database connections 
class DatabaseManager: 
    def __init__(self):
        self.dbPath = databasePath
        self.connection = None 

    # Creating a method to connect to the database 
    def connect(self): 
        # Establish a connection to the SQLite database 
        # Using try except block 
        try: 
            # if the connection is not established, create a 
            # new connection 
            if self.connection is None: 
                # Connect to the SQLite database 
                self.connection = sqlite3.connect(self.dbPath, check_same_thread=False)

                # Display the connection status 
                print("[INFO]: Connected to the database")

            # Return the connection object 
            return self.connection

        # Except the connection is an error 
        except Exception as error: 
            # Could not connect to the database 
            return str(error); 

    # Close the database connection 
    def close(self): 
        # Close the database connection 
        if self.connection: 
            # Close the connection 
            self.connection.close() 
            self.connection = None 

    # Get the user by email only 
    def verifyUserByEmail(self, email): 
        # Connecting to the database 
        conn = self.connect()
        cursor = conn.cursor() 

        # Setting the sql query 
        query = "SELECT password, email FROM users WHERE email = ?"
        cursor.execute(query, (email, ))

        # Fetch one result for the query 
        result = cursor.fetchone() 

        # Return the result 
        return result
    
    # Get the user balance
    def getUserDetails(self, email):
        # Connecting to the database 
        conn = self.connect()
        cursor = conn.cursor()

        # Setting the sql query 
        query = "SELECT id, fullname, email, balance, totalInvested, totalEarnings FROM users WHERE email = ?"
        cursor.execute(query, (email, ))

        # Fetch one result for the query 
        result = cursor.fetchall() 

        # Return the result 
        return result 
    
    # Get the miners data
    def getMinersData(self, email): 
        # Connecting to the database 
        conn = self.connect()
        cursor = conn.cursor()

        # Setting the sql query 
        query = "SELECT email, minerName, cycleDays, daysRemaining, projectedReturn, status FROM miners WHERE email = ?"
        cursor.execute(query, (email, ))

        # Fetch one result for the query 
        result = cursor.fetchall() 

        # Return the result 
        return result 
    
    # Save a user to the database 
    def saveUser(self, fullname, email, 
                password, balance=0.00, totalInvested=0.0,
                totalEarnings=0.00): 
        # Connect to the database 
        conn = self.connect() 
        cursor = conn.cursor() 

        # Getting the user data 
        userData = (fullname, email, password, balance, totalInvested, totalEarnings)

        # SQL query to save the users 
        query = "INSERT INTO users (fullname, email, password, balance, totalInvested, totalEarnings) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, userData)

        # Getting the miner email address 
        emailAddress = self.getUserDetails(email=email)[0][2]

        # Setting the miners data 
        minersData = (emailAddress, "", "", "", 5000, "")

        # Setting the SqL query to save the miners data 
        query = "INSERT INTO miners (email, minerName, cycleDays, daysRemaining, projectedReturn, status) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, minersData)

        # Commit the changes 
        conn.commit() 

        # Return the data 
        return {
            "message": "Sucessful saved the user data", 
            "status": "success", 
            "statusCode": 200
        }