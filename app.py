import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

from helpers import *

#Configure App
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

#Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


#Routes
@app.route("/")
def index():
    """Homepage. Displays project info and financial dashboard."""
    return render_template("index.html")


@app.route("/setup", methods=["GET", "POST"])
def setup():
    """Starts a new project. Initializes budgets and project info."""
    if request.method == "POST":
        
        return render_template("setup.html")

    if request.method == "GET":

        return render_template("setup.html")

@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    """Presents a record of all transactions."""
    if request.method == "POST":
        
        return render_template("transactions.html")

    if request.method == "GET":
        
        return render_template("transactions.html")

