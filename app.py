import random
import datetime
import csv
import time
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///LuckyChick.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def home():
       user_id = session["user_id"]

       cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
       cash = cash_db[0]["cash"]
       if cash < 0:
           db.execute("UPDATE users SET cash = 0 WHERE id = ?", user_id)
       date = datetime.datetime.now()
       year = date.year
       day = date.day
       time = date.strftime("%H:%M:%S")
       MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",  "November", "December"]
       month = date.month
       dayz = date.strftime("%A")
       cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
       user_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
       user = user_db[0]["username"]
       cash = cash_db[0]["cash"]
       if month == 1:
           monthz = MONTHS[0]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 2:
           monthz = MONTHS[1]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 3:
           monthz = MONTHS[2]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 4:
           monthz = MONTHS[3]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 5:
           monthz = MONTHS[4]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 6:
           monthz = MONTHS[5]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 7:
           monthz = MONTHS[6]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 8:
           monthz = MONTHS[7]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 9:
           monthz = MONTHS[8]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 10:
           monthz = MONTHS[9]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 11:
           monthz = MONTHS[10]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)
       elif month == 12:
           monthz = MONTHS[11]
           return render_template("home.html", cash=cash, user=user, year=year, day=day, dayz=dayz, monthz=monthz, time=time)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    username_db = db.execute("SELECT username FROM users")

    if not username:
        return apology("Username field required")
    if not password:
        return apology("Password field required")
    if confirmation != password:
        return apology("Password and Password Confirmation do not match")
    if username in username_db:
        return apology("username Already Taken")

    hash = generate_password_hash(password)

    try:
        new_user = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
        )
    except:
        return apology("Username already taken")

    session["user_id"] = new_user
    user_id = session["user_id"]
    db.execute("INSERT INTO chicks (chick, happy_chick, orange_chick, excited_chick, red_chick, pink_chick, blue_chick, chick_id, cost_chick, cost_happy_chick, cost_orange_chick, cost_excited_chick, cost_red_chick, cost_pink_chick, cost_blue_chick) VALUES (0, 0, 0, 0, 0, 0, 0, ?, 150.00, 200.00, 300.00, 450.00, 800.00, 1000.00, 2000.00)", user_id)
    return redirect("/")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/index")
@login_required
def index():
    user_id = session["user_id"]
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    if cash < 0:
        db.execute("UPDATE users SET cash = 0 WHERE id = ?", user_id)
    return render_template("index.html")

@app.route("/inventory")
@login_required
def inventory():
    user_id = session["user_id"]
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    if cash < 0:
        db.execute("UPDATE users SET cash = 0 WHERE id = ?", user_id)

    chick_db = db.execute("SELECT chick FROM chicks WHERE chick_id = ?", user_id)
    chick = chick_db[0]["chick"]
    happy_chick_db = db.execute("SELECT happy_chick FROM chicks WHERE chick_id = ?", user_id)
    happy_chick = happy_chick_db[0]["happy_chick"]
    orange_chick_db = db.execute("SELECT orange_chick FROM chicks WHERE chick_id = ?", user_id)
    orange_chick = orange_chick_db[0]["orange_chick"]
    excited_chick_db = db.execute("SELECT excited_chick FROM chicks WHERE chick_id = ?", user_id)
    excited_chick = excited_chick_db[0]["excited_chick"]
    red_chick_db = db.execute("SELECT red_chick FROM chicks WHERE chick_id = ?", user_id)
    red_chick = red_chick_db[0]["red_chick"]
    pink_chick_db = db.execute("SELECT pink_chick FROM chicks WHERE chick_id = ?", user_id)
    pink_chick = pink_chick_db[0]["pink_chick"]
    blue_chick_db = db.execute("SELECT blue_chick FROM chicks WHERE chick_id = ?", user_id)
    blue_chick = blue_chick_db[0]["blue_chick"]


    return render_template("inventory.html",
                           chick=chick,
                           happy_chick=happy_chick,
                           orange_chick=orange_chick,
                           excited_chick=excited_chick,
                           red_chick=red_chick,
                           pink_chick=pink_chick,
                           blue_chick=blue_chick)

@app.route("/hatch")
@login_required
def hatch():
    user_id = session["user_id"]
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    if cash < 0:
        db.execute("UPDATE users SET cash = 0 WHERE id = ?", user_id)
    return render_template("hatch.html")

@app.route("/hatch-confirm")
@login_required
def hatch_confirm():
    user_id = session["user_id"]
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    if cash < 0:
        db.execute("UPDATE users SET cash = 0 WHERE id = ?", user_id)
    return render_template("hatch-confirm.html")

@app.route("/hatched")
@login_required
def hatched():
    user_id = session["user_id"]
    chick = None
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    if cash == 0:
        return apology("Not Enough Cash")

    if cash < 0:
         db.execute("UPDATE users SET cash = 0 WHERE id = ?", user_id)

    user_id = session["user_id"]
    chick = None
    com_chick = None
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    number1 = random.random()
    number2 = random.random()
    number3 = random.random()
    number4 = random.random()
    number5 = random.random()
    number6 = random.random()
    number7 = random.random()

    Chicks = [
        "chick",
        "happy_chick",
        "orange_chick",
        "excited_chick",
        "red_chick",
        "pink_chick",
        "blue_chick"
    ]


    Cost = [
        150.00,
        200.00,
        300.00,
        450.00,
        800.00,
        1000.00,
        2000.00
    ]


    update_cash = cash - 200.00

    db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

    if number1 >= 0.4:
        if number2 >= 0.5:
            if number3 >= 0.5:
                if number4 >= 0.5:
                    if number5 >= 0.5:
                        if number6 >= 0.5:
                            if number7 >= 0.5:
                                chick = 'Blue Chick'
                                com_chick = 'blue_chick'
                        else:
                            chick = 'Pink Chick'
                            com_chick = 'pink_chick'
                    else:
                        chick = 'Red Chick'
                        com_chick = 'red_chick'
                else:
                    chick = 'Excited Chick'
                    com_chick = 'excited_chick'
            else:
                chick = 'Orange Chick'
                com_chick = 'orange_chick'
        else:
            chick = 'Happy Chick'
            com_chick = 'happy_chick'
    else:
        chick = "Chick"
        com_chick = 'chick'

    db.execute("UPDATE chicks SET ? = 1 WHERE chick_id = ?", com_chick, user_id)


#    update_chick_db = db.execute("SELECT * FROM chicks WHERE chick_id = ?", user_id)

# problem = the column in chicks start count from 0

## may be used in the future --- OR NEVER.


#    update_chick1 = update_chick_db[0]["chick"] + 1
#    update_chick2 = update_chick_db[0]["happy_chick"] + 1
#    update_chick3 = update_chick_db[0]["orange_chick"] + 1
#    update_chick4 = update_chick_db[0]["excited_chick"] + 1
#    update_chick5 = update_chick_db[0]["red_chick"] + 1
#    update_chick6 = update_chick_db[0]["pink_chick"] + 1
#    update_chick7 = update_chick_db[0]["blue_chick"] + 1


#    if com_chick == "chick":
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, update_chick1, user_id)

#    elif com_chick == "happy_chick":
#        sum_chick = update_chick2 + 1
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, sum_chick, user_id)

#    elif com_chick == "orange_chick":
#        sum_chick = update_chick3 + 1
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, sum_chick, user_id)

#    elif com_chick == "excited_chick":
#        sum_chick = update_chick4 + 1
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, sum_chick, user_id)

#    elif com_chick == "red_chick":
#        sum_chick = update_chick5 + 1
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, sum_chick, user_id)

#    elif com_chick == "pink_chick":
#        sum_chick = update_chick6 + 1
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, sum_chick, user_id)

#    elif com_chick == "blue_chick":
#        sum_chick = update_chick7 + 1
#        db.execute("UPDATE chicks SET ? = ? + ? WHERE chick_id = ?", com_chick, com_chick, sum_chick, user_id)

    return render_template("hatched.html", chick=chick)


@app.route("/news")
@login_required
def news():
    return render_template("news.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    user_id = session["user_id"]

    Chick1 = db.execute("SELECT chick FROM chicks WHERE chick_id = ?", user_id)
    Happy_chick1 = db.execute("SELECT happy_chick FROM chicks WHERE chick_id = ?", user_id)
    Orange_chick1 = db.execute("SELECT orange_chick FROM chicks WHERE chick_id = ?", user_id)
    Excited_chick1 = db.execute("SELECT excited_chick FROM chicks WHERE chick_id = ?", user_id)
    Red_chick1 = db.execute("SELECT red_chick FROM chicks WHERE chick_id = ?", user_id)
    Pink_chick1 = db.execute("SELECT pink_chick FROM chicks WHERE chick_id = ?", user_id)
    Blue_chick1 = db.execute("SELECT blue_chick FROM chicks WHERE chick_id = ?", user_id)

    chick1 = Chick1[0]["chick"]
    happy_chick1 = Happy_chick1[0]["happy_chick"]
    orange_chick1 = Orange_chick1[0]["orange_chick"]
    excited_chick1 = Excited_chick1[0]["excited_chick"]
    red_chick1 = Red_chick1[0]["red_chick"]
    pink_chick1 = Pink_chick1[0]["pink_chick"]
    blue_chick1 = Blue_chick1[0]["blue_chick"]

    Chicks = [
        "chick",
        "happy_chick",
        "orange_chick",
        "excited_chick",
        "red_chick",
        "pink_chick",
        "blue_chick"
    ]


    Cost = [
        150.00,
        200.00,
        300.00,
        450.00,
        800.00,
        1000.00,
        2000.00
    ]
    if request.method == "GET":
        user_id = session["user_id"]
        db.execute(
            "SELECT * FROM chicks WHERE chick_id = ?",
            user_id,
        )
        return render_template(
            "sell.html", Chicks=Chicks,
        )
    else:
        chick = request.form.get("Chicks")
        if chick not in Chicks:
            return apology("Chick Field Required")

        if chick == None:
            return apology("The Chick You've inputted Doesn't Exist")

        cost_chick = "cost_" + chick

        if chick == "chick":
            if chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 150 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

        if chick == "happy_chick":
            if happy_chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 200 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

        if chick == "orange_chick":
            if orange_chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 300 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

        if chick == "excited_chick":
            if excited_chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 450 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

        if chick == "red_chick":
            if red_chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 800 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

        if chick == "pink_chick":
            if pink_chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 1000 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

        if chick == "blue_chick":
            if blue_chick1 > 0:
                db.execute("UPDATE users SET cost_chick = 2000 WHERE id = ?", user_id)
                db.execute("UPDATE users SET cash = cash + cost_chick WHERE id = ?", user_id)
                db.execute("UPDATE chicks SET ? = 0 WHERE chick_id = ?", chick, user_id)
                flash("Sold!")
                return redirect("/")
            else:
                return apology("You do not have this type of chick")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        new = request.form.get("new")
        confirmation_new = request.form.get("confirmation_new")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        elif not new:
            return apology("must provide new password", 403)

        elif not confirmation_new:
            return apology("Must provide confirmation")

        elif confirmation_new != new:
            return apology("New Password And New Password Confirmation Does Not Match")

        elif password == new:
            return apology("Password and New Password Cannot Be The Same")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        hash = generate_password_hash(new)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        db.execute("UPDATE users SET hash = ? WHERE username = ?", hash, username)
        # Redirect user to home page
        return render_template("passreset.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")


@app.route("/leaks")
@login_required
def leaks():
    return render_template("leaks.html")


@app.route("/passwordgen")
def passwordgen():
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWSYZ"
    lowercase_letters = uppercase_letters.lower()
    digits = "1234567890"
    symbols = "~`!@#$%^&*()_-+={}[]£,./?><;:\ "


    upper, lower, nums, syms =  True, True, True, True

    all = ""

    if upper:
        all += uppercase_letters
    if lower:
        all += lowercase_letters
    if nums:
        all += digits
    if syms:
        all += symbols


    length = random.randint(10, 20)
    amount = 1

    for i in range(amount):
        password = "".join(random.sample(all, length))

    return render_template("passwordgen.html", password=password)


@app.route("/freegift")
@login_required
def freegift():
    user_id = session["user_id"]
    Chick1 = db.execute("SELECT chick FROM chicks WHERE chick_id = ?", user_id)
    Happy_chick1 = db.execute("SELECT happy_chick FROM chicks WHERE chick_id = ?", user_id)
    Orange_chick1 = db.execute("SELECT orange_chick FROM chicks WHERE chick_id = ?", user_id)
    Excited_chick1 = db.execute("SELECT excited_chick FROM chicks WHERE chick_id = ?", user_id)
    Red_chick1 = db.execute("SELECT red_chick FROM chicks WHERE chick_id = ?", user_id)
    Pink_chick1 = db.execute("SELECT pink_chick FROM chicks WHERE chick_id = ?", user_id)
    Blue_chick1 = db.execute("SELECT blue_chick FROM chicks WHERE chick_id = ?", user_id)

    chick1 = Chick1[0]["chick"]
    happy_chick1 = Happy_chick1[0]["happy_chick"]
    orange_chick1 = Orange_chick1[0]["orange_chick"]
    excited_chick1 = Excited_chick1[0]["excited_chick"]
    red_chick1 = Red_chick1[0]["red_chick"]
    pink_chick1 = Pink_chick1[0]["pink_chick"]
    blue_chick1 = Blue_chick1[0]["blue_chick"]
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    if cash > 199 and chick1 == 1 or happy_chick1 == 1 or orange_chick1 == 1 or excited_chick1 == 1 or red_chick1 == 1 or pink_chick1 == 1 or blue_chick1 == 1:
        flash("You already have enough money to buy an egg and a chick/chicks to sell to earn money. (You will need to have less than $200 and have no chicks to excess this page)")
        return redirect("/")
    elif cash > 199:
        flash("You already have enough money to buy an egg. (You will need to have less than $200 and have no chicks to excess this page)")
        return redirect("/")

    elif chick1 == 1 or happy_chick1 == 1 or orange_chick1 == 1 or excited_chick1 == 1 or red_chick1 == 1 or pink_chick1 == 1 or blue_chick1 == 1:
        flash("You already have a chick/chicks to sell to earn money. (You will need to have less than $200 and have no chicks to excess this page)")
        return redirect("/")
    else:
        x = 10
        chick = ""
        com_chick = ""

        number1 = random.random()
        number2 = random.random()
        number3 = random.random()
        number4 = random.random()
        number5 = random.random()
        number6 = random.random()
        number7 = random.random()

        if number1 >= 0.25:
            if number2 >= 0.3:
                if number3 >= 0.4:
                    if number4 >= 0.5:
                        if number5 >= 0.6:
                            if number6 >= 0.7:
                                if number7 >= 0.8:
                                    chick = "Massive Gift"
                                    com_chick = 500
                            else:
                                chick = "Large Gift"
                                com_chick = 350
                        else:
                            chick = "Big Gift"
                            com_chick = 250
                    else:
                        chick = 'Medium Gift'
                        com_chick = 150
                else:
                    chick = "Small Gift"
                    com_chick = 100
            else:
                chick = "Tiny Gift"
                com_chick = 75
        else:
            chick = "Mini Gift"
            com_chick = 50

        update_cash = cash + com_chick

        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        flash(f"You got a {chick}! (${com_chick}.00)")

        return redirect("/")
