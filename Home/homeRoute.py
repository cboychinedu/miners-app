#!/usr/bin/env python3 

# Importing the necssary modules 
import os 
from datetime import datetime
from flask import request, Blueprint, render_template, redirect, url_for, jsonify

# Creating the blueprint object 
home = Blueprint('home', __name__, 
                template_folder='templates', 
                static_folder='static')


# Creating the home page 
@home.route("/", methods=["GET", "POST"])
def HomePage(): 
    # Rendering the html template file 
    return render_template("home.html"); 


# Creating a route for the how it works page 
@home.route('/how-it-works')
def howItWorks():
    """
    Renders the How It Works page, explaining the process.
    """
    return render_template('howItWorks.html')

# Creating the route for the about page 
@home.route('/about')
def aboutPage():
    """
    Renders the About Us page.
    """
    # Rendering the about page 
    return render_template('about.html')


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
        {"name": "PRO IV", "price": "28,500", "income": "37,000", "days": 40, "desc": "Ultra Hash Rate. Maximum capacity with high initial investment.", "accent": "accent"}, # Note: PRO IV accent border
    ]

    # Rendering the component
    return render_template('miners.html', miners=minerData)


# Creating the login page 
@home.route("/login", methods=["POST", "GET"])
def LoginPage(): 
    # IF the request is a post request 
    if request.method == "POST": 
        pass 

    else: 
        # Render the login page 
        return render_template('login.html')
    

# Creating the sign up route 
@home.route("/signup", methods=["GET", "POST"])
def SignUp(): 
    # if the request is a post request 
    if request.method == "POST": 
        pass 

    # Else 
    else: 
        # Render the signup page 
        return render_template('signup.html')