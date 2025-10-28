#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import jwt 
import datetime 
from jwt import ExpiredSignatureError, InvalidTokenError
from flask import request, Blueprint, render_template, jsonify, redirect, url_for

# Creating the blueprint object 
dashboard = Blueprint('dashboard', __name__,
                    template_folder='templates', 
                    static_folder='static')

# Getting the secret key 
secretKey = os.getenv("SECRET_KEY")

# Creating the dashbaord home page 
@dashboard.route('/', methods=['GET', 'POST'])
def HomePage(): 
    # Getting the user's token 
    token = request.cookies.get("xAuthToken") 

    # if the token is not present, redirect the user to the home page 
    if not token: 
        return redirect(url_for('home.LoginPage'))
    
    # else if the token was correct, decode the token and save 
    # the user email 
    else: 
        # Decode the jwt token using try catch block 
        try:
            # Decode the token 
            decoded = jwt.decode(token, secretKey, algorithms=["HS256"])
            userEmail = decoded.get("email")

            # Rendering the html template file 
            return render_template('dashboardHome.html', email=userEmail)
        
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
