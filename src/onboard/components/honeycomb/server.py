from flask import Flask, render_template, redirect
import skyforce
app = Flask(__name__)
from components import var
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
@app.route
def medical():
    return render_template("Medical.html")
@app.route('/guidance')
def guidance():
    # @NOTE: keep this here to tell astronauts guidance was migrated to another system
    return render_template("migrated/guidance.html")
@app.route('/games')
def games_home():
    return render_template("games/home.html")

app.run()