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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage. Displays project info and financial dashboard."""

    if request.method == "POST":
        return render_template("index.html")

    if request.method == "GET":
        # Check if the project has already been setup. Redirects to setup page. 
        if not is_setup():
            return render_template("setup.html", message = "Please set up project first.")
        budgets = db.execute("SELECT letters, amount FROM budgets")
        x_vals = []
        y_vals = []

        for budget in budgets:
            x_vals.append(budget["letters"])
            y_vals.append(budget["amount"])
        
        colors = ["#FF6666", "#FFB266", "#009999" , "#66B2FF", "#6666FF"]
        return render_template("index.html", xVals = x_vals, yVals = y_vals, colors = colors)


@app.route("/setup", methods=["GET", "POST"])
def setup():
    """Starts a new project. Initializes budgets and project info."""
    if request.method == "POST":
        # Retrieving project information inputs from forms.
        project_owner = request.form.get("owner")
        location = request.form.get("location")
        date = request.form.get("date")
        duration = request.form.get("duration")

        # Checks for an incomplete project info input section. 
        if None in {project_owner, location, date, duration}:
            return render_template("setup.html", message = "Form is not complete. Please try again.")

        # Budget section inputs
        budget_dict=[]
        # Hard coded length 5, same hard-coded setup in setup.html
        for i in range(5):
            form_letter = "letter " + str(i)
            form_description = "description " + str(i)
            form_budget = "budget " + str(i)
            letter = request.form.get(form_letter)
            description = request.form.get(form_description)
            budget = request.form.get(form_budget)
            if not letter == "" and not budget == "":
                budget_dict.append({"letter": letter, "description": description, "budget": budget})
        
        # Update database with the inputs
        db.execute("INSERT INTO info (owner_name, location, start_date, project_duration, original_budget) VALUES (?, ?, ?, ?)", project_owner, location, date, duration)
        
        for row in budget_dict:
            db.execute("INSERT INTO budgets (letters, description, amount) VALUES (?, ?, ?)", row["letter"], row["description"], row["budget"])
            db.execute("INSERT INTO original_budgets (letters, description, amount) VALUES (?, ?, ?)", row["letter"], row["description"], row["budget"])

        return render_template("index.html", confirmation_message = "Project setup is successful.")

    if request.method == "GET":
        if is_setup():
            return render_template("index.html", confirmation_message = "Project is already set up.")
        else:
            return render_template("setup.html")

@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    """Presents a record of all transactions."""

    if request.method == "POST":
        # Receive form inputs
        letter = request.form.get("letter").upper()
        amount = request.form.get("amount")
        notes = request.form.get("notes")

        # Validate inputs
        budget_letters = db.execute("SELECT letters FROM budgets")
        letters = []

        for i in budget_letters:
            letters.append(i["letters"])

        if not letter in letters:
            return apology("Budget letter is unavailable.")
        
        try: 
            amount = float(amount)
        except:
            return apology("Invalid amount")

        updated_budget = calc_budget(letter, amount)
        if updated_budget < 0:
            return apology("Insufficient balance.")

        # Update databases and present the latest data.
        db.execute("INSERT INTO transactions (trans_type, amount, letter, notes) VALUES ('Deduct', ?, ?, ?)", (amount * -1), letter, notes)
        return redirect("/transactions")

    if request.method == "GET":
        # Check if the project has already been setup. Redirects to setup page. 
        if not is_setup():
            return render_template("setup.html", message = "Please set up project first.")
        transactions = db.execute("SELECT *, date(timestamp) FROM transactions ORDER BY trans_id")
        return render_template("transactions.html", transactions = transactions)
