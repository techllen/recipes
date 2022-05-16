from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import user,recipe

# this route receives recipes from the database
@app.route("/recipes/<int:id>")
def get_recipe(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data_user = {
            "id": session["user_id"]
        }
        data_recipe = {
            "id" : id
        }
        recipe_from_db = recipe.Recipe.get_one_recipe_by_id(data_recipe)
        # in case no recipe
        if recipe_from_db == False:
            return render_template ("get_recipe.html",user_to_display = user.User.get_one_user_by_id(data_user))
        # if there is a recipe
        else:
            return render_template ("get_recipe.html",recipe_to_display = recipe_from_db,user_to_display = user.User.get_one_user_by_id(data_user))

# this sends the user to create recipe page
@app.route("/recipes/new")
def recipe_new():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        return render_template("create_recipe.html")

# this route creates recipe entry to the database
@app.route("/create_recipe",methods = ["POST"])
def create_recipe():
    # print (recipe.Recipe.validate_recipe(request.form))
    # validating inputs from recipe form
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    else:
        # retrieve user id and add it as a foreign key in the recipes table
        user_id = session["user_id"]
        
        data = {
            "name" : request.form["name"],
            "description" : request.form["description"],
            "instructions" : request.form["instructions"],
            "under_thirty_minutes" : request.form["under_thirty_minutes"],
            "date_made_on" : request.form["date_made_on"],
            "user_id" : user_id
        }
        
        # save the recipe to the database
        recipe.Recipe.create_recipe(data)
        # redirect user to dashboard
        return redirect ("/dashboard")
    
# this method retrieves recipe in the database
@app.route("/recipes/edit/<int:id>")
def retrieve_recipe_for_editing(id):
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
            "id" : id,
        }
        recipe_from_db = recipe.Recipe.get_one_recipe_by_id(data)
        # in case no recipe
        if recipe_from_db == False:
            return render_template ("edit_recipe.html")
        # if there is a recipe
        else:
            return render_template ("edit_recipe.html",recipe_to_display = recipe_from_db)
# this route update the recipe in the database
@app.route("/edit_recipe",methods = ["POST"])
def update_recipe():
    id = request.form["recipe_id"]
    # validating inputs from recipe form
    if not recipe.Recipe.validate_recipe_on_edit(request.form):
        return redirect(f"/recipes/edit/{id}")
    else:
        # getting all info from the edit form
        data = {
            "id" : request.form["recipe_id"],
            "name" : request.form["name"],
            "description" : request.form["description"],
            "instructions" : request.form["instructions"],
            "under_thirty_minutes" : request.form["under_thirty_minutes"],
            "date_made_on" : request.form["date_made_on"],
        }
        recipe.Recipe.update_recipe(data)
        
        return redirect ("/dashboard")
    

# this method delete recipe in the database
@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    data = {
        "id" : id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect ("/dashboard")