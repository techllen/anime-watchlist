from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models.user import User
from flask_app.models.anime import Anime
from flask_app.models.thought import Thought
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# this route redirect users to the register page
@app.route("/")
def home():
    # return render_template("login.html")
    return render_template("login.html")


# this route redirect users to the dashboard page
@app.route("/dashboard")
def dashboard_page():
    # check if user is logged in
    if 'user_id' in session:
        user_data = {
            'id': session['user_id']
        }
        user = User.getOne(user_data)
        anime = Anime.getAllAnimes()
        genres = ["Action","Adventure","Comedy","Drama","Fantasy","Isekai","Music","Romance","Scifi","Seinen","Shojo","Shonen","Slice Of Life","Sports","Supernatural","Thriller"]
        return render_template("dashboard.html", user=user, animes=anime, genres=genres)
    else: 
        return redirect("/")


# this route handles user registration
@app.route("/register", methods = ["POST"])
def register():
    #validating user inputs
    if not User.validateRegister(request.form):
        # if any user input is invalid send the user to home page
        return redirect("/")
    else:
        #hashing passwords
        password_hash = bcrypt.generate_password_hash(request.form["password"])
        # print(password_hash)
        # dictionary to carry user input data
        data = {
            "username": request.form["username"],
            "email": request.form["email"],
            #assigning the password hash into the password dictionary key    
            "password": password_hash
        }
        # saving the data
        user_id = User.createOne(data)
        # assigning session to the user
        session["user_id"] = user_id
        # redirecting the user to the dashboard
        return redirect("/dashboard")

# this route handles user login
@app.route("/login", methods = ["POST"])
def login():
    user_data = {
        "email": request.form["email"],
    }
    # validating the user
    found_user = User.validate_login(user_data)
    # when email is not found take the user back to the register page
    if not found_user:
        return redirect("/")
    else:
        # retrieve the user data
        user_in_db = User.getByEmail(user_data)
        # when password dont match take user back to the login page
        if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
            # getting the flash messages
            User.validate_login(user_data)
            return render_template("login.html")
        else:
            #assigning session to the user
            session["user_id"] = user_in_db.id
            # redirecting the user to the dashboard
            return redirect("/dashboard")


# this route handles logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

