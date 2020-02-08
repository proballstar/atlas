from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/Rocket')
def rocket():
    return render_template("rocket.html")

app.run()