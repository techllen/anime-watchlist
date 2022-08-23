from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models.user import User
from flask_app.models.anime import Anime
from flask_app.models.thought import Thought


# this route redirect users to the add thought page(add_thought.html)
@app.route("/thought/<int:id>/new")
def new_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        anime_data = {
            "id": id
        }
        anime = Anime.getAnime(anime_data)
        return render_template("add_thoughts.html", anime=anime)

    
# this route handles validation and saving the thought to the database, placed in the add_thought.html action attr...it receives anime_id as variable from front end
@app.route("/thought/<int:id>/add", methods = ["POST"])
def add_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        # validate user inputs
        user_inputs = request.form
        # print(user_inputs)
        
        if not Thought.thoughtValidation(user_inputs):
            # if any user input is invalid send the user to the add new thought page
            return redirect("/dashboard")
        else:
            # dict to carry thought data
            thought_data = {
                "anime_id" : id,
                "thoughts" : request.form["thoughts"],
                "episodeNum" : request.form["episodeNum"],
                "seasonNum" : request.form["seasonNum"]
            }
            # save the thought data
            Thought.save(thought_data)
            return redirect(f"/anime/{id}")
        

# this route redirect users to the edit thought page(edit_thought.html)
@app.route("/thought/<int:id>/edit")
def edit_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        thought_data = {
            "id" : id
        }
        # retrieving a thought we want to edit from db
        thought_from_db = Thought.getById(thought_data)
        return render_template("edit_thoughts.html" ,thought = thought_from_db)
    
# this route updates edited thought data in the database
@app.route("/thought/<int:id>/update", methods = ["POST"])
def update_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:        
        thought_data = {
            "id" : id,
            "thoughts" : request.form["thoughts"]
        }
        # updating the database
        Thought.update(thought_data)
        # back to the dashboard
        return redirect("/dashboard")

# this route deletes thoughts as requested by the user
@app.route("/thought/<int:id>/delete")
def delete_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        thought_data = {
            "id" : id
        }
        # deleting a specific thought
        Thought.delete(thought_data)
        # back to the dashboard
        return redirect("/dashboard")