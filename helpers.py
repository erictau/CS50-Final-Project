import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL

db = SQL("sqlite:///budget.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def calc_budget(letter, transaction_bal):
    """Calculates the remaining budget of a letter"""
    orig_bal = db.execute("SELECT amount FROM budgets WHERE letters = ?", letter)[0]["amount"]
    new_bal = float(orig_bal) - float(transaction_bal)
    return new_bal

def is_setup():
    """Checks if the project has been setup yet."""
    if len(db.execute("SELECT * FROM info")):
        return True
    else:
        return False

def clear_project():
    """Clears databases and resets the project."""
    db.execute("DELETE FROM info")
    db.execute("DELETE FROM budgets")
    db.execute("DELETE FROM original_budget")
    db.execute("DELETE FROM transactions")
    print("Project Cleared")
    