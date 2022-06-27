from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models.user import User
from flask_app.models.anime import Anime
from flask_app.models.thought import Thought

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

@app.route("/anime/<int:id>/abandon")
def abandon(id):
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        anime_data = {
            "id" : id
        }
        Anime.abandon(anime_data)
        return redirect("/dashboard")
@app.route("/anime/<int:id>/abandon")

@app.route("/anime/<int:id>/complete")
def complete(id):
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        anime_data = {
            "id" : id
        }
        Anime.complete(anime_data)
        return redirect("/dashboard")

# this route handles validation and saving the anime to the database ,placed in the add_anime.html action attr
@app.route("/add_anime", methods = ["POST"])
def add_anime():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        if not Anime.animeValidation(request.form):
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
            Anime.save(anime_data)
            return redirect("/dashboard")
    
# this route redirect users to the view anime page(anime.html)
@app.route("/anime/<int:id>")
def view_anime(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        anime_data = {
            "id" : id
        }
        thought_data = {
            "anime_id" : id
        }
        # retrieving the anime we want to view from db
        anime_from_db = Anime.getAnime(anime_data)
        thoughts_from_db = Thought.getAllThoughts(thought_data)
        print(thoughts_from_db)
        return render_template("anime.html", anime=anime_from_db, thoughts=thoughts_from_db)
    
# this route redirect users to the edit anime page(edit_anime.html)
@app.route("/anime/<int:id>/edit")
def edit_anime_page(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        anime_data = {
            "id" : id
        }
        # retrieving the anime we want to edit from db
        anime_from_db = Anime.getAnime(anime_data)
        # populate the data in the edit page
        return render_template("edit_anime.html",genres = genres_array,anime = anime_from_db)
    
# this route updates edited anime data in the database
@app.route("/anime/<int:id>/update", methods = ["POST"])
def update_anime(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        if not Anime.animeValidation(request.form):
            return redirect(f'/anime/{id}/edit')
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
        Anime.update(anime_data)
        # back to the dashboard
        return redirect(f"/anime/{id}")

# this route deletes animes as requested by the user
@app.route("/anime/<int:id>/delete")
def delete_anime(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        anime_data = {
            "id" : id
        }
        # deleting a specific anime
        Anime.delete(anime_data)
        # back to the dashboard
        return redirect("/dashboard")

@app.route("/<name>")
def genreView(name):
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        genre_data = {
            "genre": name
        }
        animes = Anime.getByGenre(genre_data)
        return render_template("genre.html",animes=animes,genre=name)
