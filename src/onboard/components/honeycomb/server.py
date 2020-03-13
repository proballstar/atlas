from flask import Flask, render_template, redirect
import skyforce
app = Flask(__name__)
import sqlite3
import requests
from requests.api import request


#@TODO AARON CAN YOU MAKE A FUNCTION in status_code that sees if there is an err
def status_code():
    pass
    
# COMPLETED@TODO(aaronhma): replace pass with a function that gets the status quo (Ex. 404, 200,400) call the status code, status_code 
# for get_err, make a function that if error shows it with parsing and set a variable called err with it , replace path with it
# @TODO(create every possible error)
# @TODO(aaronhma): put a note for how to pass dev_mode and err

# @NOTE: Only use status_code function IF there is an err . once updated fully be implemented otherwise


def get_err(dev_mode, err):
    if dev_mode != False:
        e = err
        if e == "EnvironmentError":
            status_code = 100
        elif e == "AssertionError":
            status_code = 200
        elif e == "SyntaxError":
            status_code = 300
        else:
            status_code = 400
        
    else:
        status_code = 900 # @TODO(aaronhma): UPDATE to resilient code
    
    return status_code
    
#@NOTE  ROHAN ONLY for check_status def ,AARON for status_code
def check_status(status_code,err):
    if status_code == 100 or 200 or 300 or 400:
        print("err",err)
    else:
        pass
    
    


@app.route('/')
def home():
   return render_template("rocket.html")
@app.route('/homepage')
def homepage():
    c1 = "Navigation"
    c2 = "Guidiance"
    c3 = "Cooling "
    c4 = "Heater"
    c5 = "Computer"
    c6 = "Honeycomb"
    c7 = "Engine"
    c8 = "Thruster"
    c9 = "Communications "
    return render_template("home.html",c1 = c1,c2 = c2, c3 = c3, c4 = c4,c5= c5,c6=c6,c7=c7,c8=c8,c9=c9)
@app.route('/rocket')
def rocket():
 
    return render_template("rocket.html")
@app.route('/support')
def support(): 
    return render_template("support.html")
@app.route('/medical')
def medical():
    if request.method == "GET":
        # @NOTE what to do when you are using GET including adding variables
        return render_template("Medical.html")
    elif request.method == "POST":
        # @NOTE this is what happens when people submit the form 
        # @NOTE lets use python for the medical info ( log the info)
        print("POST method called!")
        
@app.route('/guidance')
def guidance():
    # @NOTE: keep this here to tell astronauts guidance was migrated to another system - APPROVED
    return render_template("migrated/guidance.html")
@app.route('/games')
def games_home():
    return render_template("games/home.html")
@app.route('/disney')
def disney():
    return render_template('disney.html')
@app.route('/apptv')
def disney():
    return render_template('appletv.html')
app.run()

