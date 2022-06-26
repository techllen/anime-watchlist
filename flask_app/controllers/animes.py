from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import anime,thought,user
from flask_app.controllers import users,thoughts

# global genres array
genres_array = ["Action","Adventure","Comedy","Drama","Fantasy","Isekai","Music","Romance","Scifi","Seinen","Shojo","Shonen","Slice Of Life","Sports","Supernatural","Thriller"]

# this route redirect users to the add anime page(add_anime.html)
@app.route("/anime/new")
def new_anime():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        return render_template("add_anime.html",genres = genres_array)

    
# this route handles validation and saving the anime to the database ,placed in the add_anime.html action attr
@app.route("/add_anime", methods = ["POST"])
def add_anime():
    user_inputs = request.form   
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        if not anime.Anime.animeValidation(user_inputs):
            # if any user input is invalid send the user to the add new anime page
            return redirect("/anime/new")
        else:
            user_id = session.get("user_id")

            # create dict to carry user data to save in the database
            anime_data = {
            "user_id" : user_id,
            "title" :  request.form["title"],
            "episodeNum" :  request.form["episodeNum"],
            "seasons" :  request.form["seasons"],
            "statusDone" :  request.form["statusDone"],
            "startedAt" :  request.form["startedAt"], 
            "genre" :  request.form["genre"],
            "coverImg" :  request.form["coverImg"],
            }
            # save the anime data
            anime.Anime.save(anime_data)
            return redirect("/dashboard")
    
# this route redirect users to the view anime page(anime.html)
@app.route("/view_anime/<int:id>")
def view_anime(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        anime_data = {
            "id" : id
        }
        # retrieving the anime we want to view from db
        anime_from_db = anime.Anime.getAnime(anime_data)
        return render_template("anime.html",anime = anime_from_db)
    
# this route retrieves all the animes from the database
@app.route("/get_all_animes")
def get_all_animes():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        # retrieving all the anime we want to view from db
        animes_from_db = anime.Anime.getAllAnimes()
        # return render_template(,animes = animes_from_db)
        pass
    
# this route retrieves all the animes from the database added by a specific user
# @app.route("/get_all_animes_by_user_id")
# def get_all_animes_by_user_id():
#     # check if user is logged in
#     if session.get("user_id")==None: 
#         return redirect("/")
#     else:
#         user_data = {
#             "id" : session.get("user_id")
#         }
#         # retrieving all the anime we want to view from db by user id
#         # animes_from_db_by_user_id= anime.Anime.get_all_animes_by_user_id(user_data)
#         # return render_template(,animes = animes_from_db_by_user_id)
#         pass
    
# this route redirect users to the edit anime page(edit_anime.html)
@app.route("/edit_anime/<int:id>")
def edit_anime_page(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        anime_data = {
            "id" : id
        }
        # retrieving the anime we want to edit from db
        anime_from_db = anime.Anime.getAnime(anime_data)
        # populate the data in the edit page
        return render_template("edit_anime.html",genres = genres_array,anime = anime_from_db)
    
# this route updates edited anime data in the database
@app.route("/anime/<int:id>/update", methods = ["POST"])
def update_anime(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:        
        anime_data = {
        "title" :  request.form["title"],
        "episodeNum" :  request.form["episodeNum"],
        "seasons" :  request.form["seasons"],
        "statusDone" :  request.form["statusDone"],
        "startedAt" :  request.form["startedAt"], 
        "genre" :  request.form["genre"],
        "coverImg" :  request.form["coverImg"],
        "id" : id
        }
        # updating the database
        anime.Anime.update(anime_data)
        # back to the dashboard
        return redirect("/dashboard")

# this route deletes animes as requested by the user
@app.route("/delete_anime/<int:id>")
def delete_anime(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        anime_data = {
            "id" : id
        }
        # deleting a specific anime
        anime.Anime.delete(anime_data)
        # back to the dashboard
        return redirect("/dashboard")