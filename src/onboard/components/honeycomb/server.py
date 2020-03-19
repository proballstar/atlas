import sys
sys.path.append(r'C:\Users\Rohan Fernandes\python_bit\Aaron\Progects\atlas')

from flask import Flask, render_template, redirect, request
from shared import components
from shared import Gui
from shared import medical
from shared import skyforce
from shared import error

app = Flask(__name__)

    
@app.route('/')
def home():
    return render_template("rocket.html")

@app.route('/homepage')
def homepage():
    c1 = "Navigation"
    c2 = "Guidiance"
    c3 = "Cooling"
    c4 = "Heater"
    c5 = "Computer"
    c6 = "Honeycomb"
    c7 = "Engine"
    c8 = "Thruster"
    c9 = "Communications"
    return render_template("home.html",c1 = c1,c2 = c2, c3 = c3, c4 = c4,c5= c5,c6=c6,c7=c7,c8=c8,c9=c9)

@app.route('/rocket')
def rocket():
    return redirect('/')

@app.route('/support')
def support(): 
    return render_template("support.html")

@app.route('/medical')
def medical():
    if request.method == "GET":
        # @NOTE what to do when you are using GET including adding variables
        medical.__init__()
        return render_template("Medical.html")
    elif request.method == "POST":
        # @NOTE this is what happens when people submit the form 
        # @NOTE lets use python for the medical info ( log the info)
        medical.post()
        print("POST method called!")
        return render_template("Medical.html")
        
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

@app.route('/appletv')
def appletv():
    return render_template('appletv.html')

app.run(port=7777) 

del app
