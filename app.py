import os
import requests
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///exchange.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    result = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=user_id)

    # Check if there are any rows
    if not result:
        return apology("User not found", 404)

    # Fetch the first row (if any)
    user_info = result[0]
    print(user_info)

    return render_template('index.html', user_info=user_info)

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == "POST":
        # Fetch fresh conversion rates
        conversion_rates = get_exchange_data()

        json_data = request.form.get('json')

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON data. Please provide valid JSON"})

        amount_str = data.get('amount')
        from_currency = data.get('from_currency')
        to_currency = data.get('to_currency')

        # Perform the conversion
        converted_amount = float(amount_str) * (conversion_rates[to_currency] / conversion_rates[from_currency])

        data = {
            "converted_amount" : converted_amount
        }

        db.execute("""INSERT INTO transactions (user_id, CurrentCurrency, NewCurrency, cash, conversion_rate)
        VALUES (:user_id, :current_currency, :new_currency, :cash, :conversion_rate)""",
        user_id=session["user_id"], current_currency=from_currency, new_currency=to_currency, cash=amount_str, conversion_rate=float(conversion_rates[to_currency]))

        return jsonify(data)

# Configure CS50 Library to use SQLite database
def get_exchange_data():
    url = 'https://v6.exchangerate-api.com/v6/5cf07c0e1450306c4e495730/latest/USD'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('conversion_rates', {})
    else:
        return {}

conversion_rates = get_exchange_data()

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Enable user to buy a stock."""

    # POST
    if request.method == "POST":
        # Validate form submission
        if not request.form.get("curr"):
            return apology("missing input")
        elif not request.form.get("curr").isdigit():
            return apology("please input digit")
        amount = int(request.form.get("curr"))
        if amount < 0:
            return apology("please input nonnegative amount")

        # Record purchase
        db.execute("""INSERT INTO transactions (user_id, CurrentCurrency, NewCurrency, cash, conversion_rate)
        VALUES (:user_id, :current_currency, :new_currency, :cash, :conversion_rate)""",
                   user_id=session["user_id"], current_currency="n/a", new_currency="n/a", cash=amount, conversion_rate=0)

        # Deduct cash
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :id",
                   amount=amount, id=session["user_id"])

        # Display portfolio
        flash("Added!")
        return redirect("/")

    # GET
    else:
        return render_template("add.html")

@app.route("/history")
@login_required
def history():
    """Display user's history of transactions."""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("firstname"):
            return apology("missing firstname")
        if not request.form.get("lastname"):
            return apology("missing lastname")

        if not request.form.get("username"):
            return apology("missing username")

        if not request.form.get("password"):
            return apology("missing password")

        if not request.form.get("confirmation"):
            return apology("missing confirmation")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match, try again.", 400)
        hashed_password = generate_password_hash(request.form.get("password"))
        print(type(hashed_password))
        try:
            id = db.execute("INSERT INTO users (firstname, lastname, username, hash) VALUES (?, ?, ?, ?)",
                            request.form.get("firstname"), request.form.get("lastname"),
                            request.form.get("username"), hashed_password)
        except ValueError:
            return apology("username taken")
        session["user_id"] = id
        return redirect("/")
    return render_template("register.html")

@app.route('/exchange')
def confirmation():
    return render_template('exchange.html')

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
