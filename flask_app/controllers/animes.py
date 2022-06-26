from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import anime,thought,user

# this route redirect users to the add anime page(add_anime.html)
@app.route("/anime/new")
def new_anime():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        # retrieving all genres from the database
        # genres_from_db = anime.Anime.get_all_genres()
        # return render_template("add_anime.html",genres = genres_from_db)
        return render_template("add_anime.html")

    
# this route handles validation and saving the animes to the database
@app.route("/add_anime", methods = ["POST"])
def add_anime():
    # validating user inputs
    user_inputs = request.form
    if not (user_inputs):
        # if any user input is invalid send the user to home page
        return redirect("/")
    else:
        pass