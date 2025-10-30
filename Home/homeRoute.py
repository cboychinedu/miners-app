#!/usr/bin/env python3 

# Importing the necssary modules 
import os
import jwt
import bcrypt
import datetime
from Email.emailSender import SendEmail
from Database.database import DatabaseManager
from flask import request, Blueprint, render_template, jsonify, make_response, redirect, url_for

# Getting the secret key 
secretKey = os.getenv("SECRET_KEY")
domainName = os.getenv("HOST")

# Creating an instance of the database manager 
db = DatabaseManager() 

# Creating the blueprint object 
home = Blueprint('home', __name__, 
                template_folder='templates', 
                static_folder='static')


# Creating the home page 
@home.route("/", methods=["GET", "POST"])
def HomePage(): 
    # Getting the user's token 
    token = request.cookies.get("xAuthToken")

    # if the token is not present, execute the block of code below 
    if not token: 
        # Rendering the html template file 
        return render_template("home.html", isLoggedIn=False)
    
    # Else if the token is present 
    else: 
        # Get the user token and parse a value into the 
        # html document 
        return render_template("home.html", isLoggedIn=True)



# Creating a route for the how it works page 
@home.route('/how-it-works')
def howItWorks():
    """
    Renders the How It Works page, explaining the process.
    """
    # Getting the user's token 
    token = request.cookies.get("xAuthToken")

    # if the token is not present, execute the block of 
    # code below 
    if not token: 
        # Rendering the how it works html file 
        return render_template('howItWorks.html', isLoggedIn=False)
    
    # Else if the token is present
    else: 
        # Get the user token and parse the isLoggedin value as 
        # True inside the html doc
        return render_template('howItWorks.html', isLoggedIn=True)

# Creating the route for the about page 
@home.route('/about')
def aboutPage():
    """
    Renders the About Us page.
    """
    # Getting the user's token 
    token = request.cookies.get("xAuthToken")

    # if the token is not present, execute the block of 
    # code below 
    if not token: 
        # Rendering the about page 
        return render_template("about.html", isLoggedIn=False)
    
    # Else if the token is present
    else: 
        # Rendering the about page 
        return render_template('about.html', isLoggedIn=True)


# Creating the miners page 
@home.route('/miners')
def minersPage():
    """
    Renders the dedicated Miners investment tiers page.
    """
    # In a real app, you would fetch miner data from a database here
    minerData = [
        {"name": "PRO I", "price": "4,500", "income": "9,000", "days": 20, "desc": "Entry Level Mining. Perfect for new investors testing the waters.", "accent": "primary"},
        {"name": "PRO II", "price": "8,500", "income": "17,000", "days": 30, "desc": "Standard Mining Power. Higher returns for a balanced investment strategy.", "accent": "primary"},
        {"name": "PRO III", "price": "14,500", "income": "29,000", "days": 40, "desc": "Premium Hash Rate. Accelerated earnings with a longer cycle.", "accent": "primary"},
        {"name": "PRO IV", "price": "28,500", "income": "37,000", "days": 40, "desc": "Ultra Hash Rate. Maximum capacity with high initial investment.", "accent": "accent"}, \
    ]

    # Getting the user's token 
    token = request.cookies.get("xAuthToken")

    # if the token is not present, execute the block of 
    # code below 
    if not token: 
        # Rendering the miner.html template file 
        return render_template('miners.html', miners=minerData, isLoggedIn=False)
    
    # Else if the token is present, execute the 
    # Block of code below 
    else: 
        # Get the user token and parse the isLogged value 
        # inside the miners.html doc 
        return render_template('miners.html', miners=minerData, isLoggedIn=True)


# Creating the login page 
@home.route("/login", methods=["POST", "GET"])
def LoginPage(): 
    # IF the request is a post request 
    if request.method == "POST":
        # Getting the user's data 
        userData = request.get_json() 
        email = userData["email"]
        password = userData["password"]

        # using try except block to get the users 
        try: 
            # Execute the block of code below 
            # Getting the user details 
            data = db.verifyUserByEmail(email=email)

            if (data):
                # Getting the user's data 
                passwordHash = data[0]
                email = data[1]

                # Verifying the password hash 
                password = password.encode('utf-8')
                condition = bcrypt.checkpw(password, passwordHash)

                # Checking the condition if the password verification 
                # return a true value 
                if (condition):
                    # Generate a token for the user and send it back to 
                    # the client 
                    payload = {
                        "email": email, 
                        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
                    }

                    # Encoding the payload as a jwt token 
                    encodedJwt = jwt.encode(
                        payload, 
                        secretKey,
                        algorithm="HS256"
                    )

                    # Prepare the response and set the cookie 
                    responseData = make_response(jsonify({
                        "message": "Login successful!", 
                        "status": "success", 
                        "email": email 
                    }))

                    # Store JWT in HTTP-only cookie 
                    responseData.set_cookie(
                        key="xAuthToken", 
                        value=encodedJwt,
                        httponly=True, 
                        secure=False, 
                        domain=domainName,
                        samesite="Strict", 
                        max_age=86400
                    )

                    # Return the response header 
                    return responseData

                else: 
                    # Generate an error message saying the passwords are 
                    # Not correct 
                    errorMessage = { 
                        "message": "Invalid Email or Password!", 
                        "status": "error", 
                        "statusCode": 401
                    }

                    # Sending the error message
                    return jsonify(errorMessage); 

            # Else if the user is not found on the database 
            else: 
                # 
                errorMessage = {
                    "status": "error", 
                    "message": "User not registered on the database", 
                    "statusCode": 404
                }

                # Sending the error message 
                return jsonify(errorMessage); 

        # Unless exception as error, execute the block 
        # of the code below 
        except Exception as e:
            # Convert the object into a json object and 
            # Send it to the clinet 
            errorMessage = {
                "message": str(e), 
                "status": "error", 
                "statusCode": 404
            }

            # Sending back the error message 
            return jsonify(errorMessage) 

    # Else if the request was a GET request 
    else: 
        # Getting the user's token 
        token = request.cookies.get('xAuthToken')

        # If the token is present redirect the user to the 
        # Dashboard page 
        if (token): 
            # Redirect the user to the dashboard page 
            return redirect(url_for('dashboard.HomePage'))
        
        # Else if the token is not present, load the login page 
        else:
            # Render the login page 
            return render_template('login.html')
    

# Creating the sign up route 
@home.route("/signup", methods=["GET", "POST"])
def SignUp(): 
    # if the request is a post request 
    if request.method == "POST":
        # Get the user data 
        userData = request.get_json(); 

        # Getting the user password, and email address 
        fullname = userData["fullname"]
        password = userData["password"]
        email = userData['email']

        # Using try finally to get the user from the database 
        try: 
            # Checking if the user details are on the sqlite3 database 
            verifyUser = db.verifyUserByEmail(email=email)

            # if the verified user exists on the database
            if (verifyUser): 
                # Return a message that the user already exists on the database 
                errorMessage = {
                    "message": "User already exists!",
                    "status": "error", 
                    "statusCode": 400 
                }

                # Sending the error message 
                return jsonify(errorMessage); 

            # Else if the user is not found on the database, register 
            # the user and hash the user password 
            else: 
                # Hashing the user password 
                password = bytes(password.encode('utf-8'))
                passwordHash = bcrypt.hashpw(password, bcrypt.gensalt())

                # Saving the user details into the database 
                data = db.saveUser(
                    fullname=fullname,
                    email=email, 
                    password=passwordHash
                )

                # if the status message was a success 
                if (data["status"] == "success"): 
                    # Return the jsonify message 
                    sucessMessage = {
                        "message": "User registered successfully!", 
                        "status": "success", 
                        "statusCode": 200
                    }

                    # Send the message 
                    return jsonify(sucessMessage)
                
                # Else if the status message was not a success 
                else: 
                    # if the status message is not successful 
                    errorMessage = {
                        "message": "Error saving the user on the database!", 
                        "status": "error", 
                        "statusCode": 404
                    }

                    # Send the message 
                    return jsonify(errorMessage) 
        
        # On exception handle the error and send it back to the 
        # User 
        except Exception as e: 
            # Print the error message 
            print(f"[INFO]: Error {e}")

            # Return the error message 
            return jsonify({
                "message": str(e), 
                "status": "error", 
                "statusCode": 500 
            })
 

    # Else 
    else: 
        # Getting the user's token 
        token = request.cookies.get("xAuthToken")

        # if the token is present redirect the user to the 
        # Dashboard page 
        if (token): 
            # Redirect the user to the dashboard page 
            return redirect(url_for('dashboard.HomePage'))
        
        # Else if the token is not present, load the signup page 
        else: 
            # Render the signup page 
            return render_template('signup.html')
        

# Creating a route for forget password 
@home.route("/forgot-password", methods=["POST", "GET"])
def ForgotPassword(): 
    # if the request was a post request 
    if request.method == "POST": 
        # Get the json objects 
        emailData = request.get_json()

        # Getting the reveiver email 
        receiverEmail = emailData["receiverEmail"]
        senderEmail = os.getenv("senderEmail")
        appPassword = os.getenv("appPassword")

        # Sending the verification code to the email address 
        mailSender = SendEmail(senderEmail, receiverEmail, appPassword)

        # Using try except block to send the email 
        try: 
            # Send the email 
            mailSender.senderEmail() 

            # Building the response message 
            responseMessage = {
                "status": "success", 
                "message": "Email message sent", 
                "statusCode": 200
            }

            # Sending the response message 
            return jsonify(responseMessage) 

        # Except 
        except Exception as error: 
            print(error)
            # Getting the error message 
            errroMessage = {
                "status": "error", 
                "message": "Error sending the email", 
                "statusCode": 404
            }

            # Sending the response message 
            return jsonify(errroMessage)


    # Else if the request method was a get request or any other 
    # request 
    else: 
        # Render the forgot password page 
        return render_template("forgotPassword.html")
