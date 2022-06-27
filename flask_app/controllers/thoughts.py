from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models.user import User
from flask_app.models.anime import Anime
from flask_app.models.thought import Thought


# this route redirect users to the add thought page(add_thought.html)
@app.route("/thought/new")
def new_thought():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        return render_template("add_thoughts.html")

    
# this route handles validation and saving the thought to the database, placed in the add_thought.html action attr
@app.route("/add_new_thought", methods = ["POST"])
def add_thought():
    # validating user inputs
    user_inputs = request.form
    # print(user_inputs)
    
    if not Thought.thoughtValidation(user_inputs):
        # if any user input is invalid send the user to the add new thought page
        return redirect("/thought/new")
    else:
        # save the thought data
        Thought.save(user_inputs)
        return redirect("/dashboard")
    
# this route redirect users to the view thought page(thought.html)
@app.route("/view_thought/<int:id>")
def view_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        thought_data = {
            "id" : id
        }
        # retrieving the thought we want to view from db
        thought_from_db = Thought.getthought(thought_data)
        return render_template("thought.html",thought = thought_from_db)
    
# this route retrieves all the thoughts from the database
@app.route("/get_all_thoughts")
def get_all_thoughts():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:
        # retrieving all the thought we want to view from db
        # thoughts_from_db = thought.thought.getAllthoughts()
        # return render_template(,thoughts = thoughts_from_db)
        pass
    
# this route redirect users to the edit thought page(edit_thought.html)
@app.route("/edit_thought/<int:id>")
def edit_thought_page(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:    
        thought_data = {
            "id" : id
        }
        # retrieving the thought we want to edit from db
        thought_from_db = Thought.getthought(thought_data)
        # populate the data in the edit page
        return render_template("edit_thought.html",thought = thought_from_db)
    
# this route updates edited thought data in the database
@app.route("/thought/<int:id>/update", methods = ["POST"])
def update_thought(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else:        
        thought_data = {
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
        Thought.update(thought_data)
        # back to the dashboard
        return redirect("/dashboard")

# this route deletes thoughts as requested by the user
@app.route("/delete_thought/<int:id>")
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