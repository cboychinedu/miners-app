#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import jwt 
import datetime 
from Database.database import DatabaseManager
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import request, Blueprint, render_template, jsonify, redirect, url_for, make_response

# Creating an instance of the database 
db = DatabaseManager()

# Creating the blueprint object 
dashboard = Blueprint('dashboard', __name__,
                    template_folder='templates', 
                    static_folder='static')

# Getting the secret key 
secretKey = os.getenv("SECRET_KEY")

transactionData = {
    'firstname': 'John Doe',
    'email': 'john.doe@example.com',
    'balance': 'NGN 150,000.00',
    'totalInvested': 'NGN 250,000.00',
    'totalEarnings': 'NGN 50,000.00',
    'user': {
        'activeMiner': {
            'status': 'ACTIVE',
            'fullname': 'Miner PRO III',
            'cycleDays': 30,
            'daysRemaining': 8,
            'projectedReturn': '60,000.00'
        }
    },
    'transactions': [
        {'date': '2025-10-27', 'type': 'Deposit', 'amount': 'NGN 100,000.00', 'status': 'Completed', 'details': 'Bank Transfer'},
        {'date': '2025-10-25', 'type': 'Investment', 'amount': 'NGN 50,000.00', 'status': 'Completed', 'details': 'Miner Starter'},
        {'date': '2025-10-20', 'type': 'Earning', 'amount': 'NGN 5,000.00', 'status': 'Completed', 'details': 'Cycle Payout'},
        {'date': '2025-10-15', 'type': 'Withdrawal', 'amount': 'NGN 20,000.00', 'status': 'Pending', 'details': 'To Personal Account'},
    ]
}

# Creating the transaction route 
@dashboard.route('/transactions', methods=["GET", "POST"])
def TransactionPage(): 
    # Getting the user's token 
    token = request.cookies.get("xAuthToken")

    # if the token is not present, execute the block of 
    # code below 
    if not token: 
        # Redirect the user to the login page 
        return redirect(url_for('home.LoginPage'))
    
    # Else if the token is present 
    # Execute the block of code below 
    else: 
        # Render the transactions page 
        return render_template("transactionsPage.html", **transactionData)

# Adding the deposit page 
@dashboard.route('/deposit', methods=['POST', 'GET'])
def DepositPage(): 
    # Getting the user's token 
    token = request.cookies.get("xAuthToken") 

    # if the token is not present, redirect the user to the 
    # login page 
    if not token: 
        # Redirect the user to the login page 
        return redirect(url_for('home.LoginPage'))
    
    # Else if the token was correct, decode the token and 
    # save the user email 
    else: 
        # Decode the jwt token using try catch block 
        try:
            # Decode the token 
            decoded = jwt.decode(token, secretKey, algorithms=["HS256"])
            userEmail = decoded.get("email")

            # Getting the user details 
            userDetails = db.getUserDetails(userEmail)

            # Getting the user fullname 
            fullname = userDetails[0][1]

            # Rendering the html template file 
            return render_template('deposit.html', fullname=fullname)
    
        except ExpiredSignatureError: 
            # Token expired - redirect the user to the login page 
            return redirect(url_for('home.LoginPage'))
        
        # if the token is invalid 
        except InvalidTokenError: 
            # Token invalid - redirect to login page 
            return redirect(url_for('home.LoginPage'))
        
        # On error generated 
        except Exception as e: 
            # Setting the error message 
            errorMessage = {
                "message": str(e), 
                "status": "error", 
                "statusCode": 500
            }

            # Sending the error message 
            return jsonify(errorMessage) 


# Creating the dashbaord home page 
@dashboard.route('/', methods=['GET', 'POST'])
def HomePage(): 
    # Getting the user's token 
    token = request.cookies.get("xAuthToken") 

    # Mock data for the dashboard
    userData = {
        "fullname": "Jane Doe",
        "email": "xyz@gmail.com",
        "balance": "89,500",
        "totalInvested": "50,000",
        "totalEarnings": "39,500",
        "activeMiner": {
            "name": "PRO II",
            "cycleDays": 30,
            "daysRemaining": 12,
            "projectedReturn": "17,000",
            "status": "Mining"
        }
    }

    # if the token is not present, redirect the user to the home page 
    if not token: 
        # Redirect the user to the login page 
        return redirect(url_for('home.LoginPage'))
    
    # else if the token was correct, decode the token and save 
    # the user email 
    else: 
        # Decode the jwt token using try catch block 
        try:
            # Decode the token 
            decoded = jwt.decode(token, secretKey, algorithms=["HS256"])
            userEmail = decoded.get("email")

            # Getting the user details 
            userBalance = db.getUserDetails(userEmail) 

            # Getting the user details
            idValue = userBalance[0][0] 
            firstname = userBalance[0][1]
            email = userBalance[0][2]
            balance = userBalance[0][3]
            totalInvested = userBalance[0][4]
            totalEarnings = userBalance[0][5] 

            # Get the miners detal 
            minersDetail = db.getMinersData(userEmail) 

            # Rendering the html template file 
            return render_template('dashboardHome.html', 
                                firstname=firstname,
                                email=email, 
                                balance=balance, 
                                totalInvested=totalInvested,
                                totalEarnings=totalEarnings, 
                                user=userData
                            )
        
        # if the token has expired 
        except ExpiredSignatureError: 
            # Token expired - redirect to login 
            return redirect(url_for('home.LoginPage'))
        
        # if the token is invalid 
        except InvalidTokenError:
            # Token invalid - redirect to login 
            return redirect(url_for('home.LoginPage'))
        
        # On error generated 
        except Exception as e: 
            # Any unexpected error, log the error and 
            # Send it back to the user 
            return jsonify({
                "message": str(e), 
                "status": "error", 
                "statusCode": 500
            })
         

@dashboard.route('/logout', methods=['POST', 'GET'])
def LogoutPage():
    """
    Logs out the user by clearing the auth_token cookie
    """
    # Create a response that redirects to login or home
    response = make_response(redirect(url_for('home.LoginPage')))

    # Delete the cookie from the client browser
    response.set_cookie(
        key="xAuthToken",
        value="",
        expires=0,       
        httponly=True,
        secure=False,
        samesite="Strict"
    )

    # Return the response 
    return response


























# @dashboard.route('/dashboard')
# def HomePage():
#     """
#     Renders the user dashboard page, providing mock user data to the template.
    
#     This data structure is crucial as it matches the Jinja variables
#     used in the dashboard.html file.
#     """
#     # Mock data for the dashboard
#     user_data = {
#         "name": "Jane Doe",
#         "balance": "89,500",
#         "total_invested": "50,000",
#         "total_earnings": "39,500",
#         "active_miner": {
#             "name": "PRO II",
#             "cycle_days": 30,
#             "days_remaining": 12,
#             "projected_return": "17,000",
#             "status": "Mining"
#         }
#     }

#     #
#     return render_template('dashboard.html', user=user_data)
