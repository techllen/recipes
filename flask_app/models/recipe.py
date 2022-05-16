from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    # initializing database name variable
    database_name = "recipes"

    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under_thirty_minutes = data["under_thirty_minutes"]
        self.date_made_on = data["date_made_on"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
    # this method creates recipe entry in the database
    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes (name,description,instructions,under_thirty_minutes,date_made_on,user_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(under_thirty_minutes)s,%(date_made_on)s,%(user_id)s)" 
        # retrieving the id of created recipe for session
        recipe_id = connectToMySQL(Recipe.database_name).query_db(query,data)
        return recipe_id
    # this method get all recipes from our database
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"
        recipes = connectToMySQL(Recipe.database_name).query_db(query)
        recipes_to_display = []
        # checking if we found any recipe
        if len(recipes) == False:
            return None
        else:
        # turning recipe results to objects
            for recipe in recipes:
                this_recipe = cls(recipe)
                # print(this_recipe)
                recipes_to_display.append(this_recipe)
            # returning list of recipe objects
            return recipes_to_display
    # this method get all recipes from our database by the user in session
    @classmethod
    def get_all_recipes_by_a_user_id(cls,data):
        query = "SELECT * FROM recipes WHERE user_id = %(id)s"
        user_recipes = connectToMySQL(Recipe.database_name).query_db(query,data)
        user_recipes_to_display = []
        # checking if we found any recipe
        if user_recipes == False:
            return None
        else:
        # turning recipe results to objects
            for recipe in user_recipes:
                this_recipe = cls(recipe)
                # print(this_recipe)
                user_recipes_to_display.append(this_recipe)
            # returning list of recipe objects
            return user_recipes_to_display
    # this method deletes recipe entry in the database
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s" 
        recipe_id = connectToMySQL(Recipe.database_name).query_db(query,data)
    # this method get one recipe from the database
    @classmethod
    def get_one_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        recipe = connectToMySQL(Recipe.database_name).query_db(query,data)
        # print(recipe)
        # checking if we found any recipe
        if len(recipe) == False:
            return None
        else:
            return cls(recipe[0])
    # this method edit recipe entry in the database
    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s,description = %(description)s,instructions = %(instructions)s,under_thirty_minutes = %(under_thirty_minutes)s,date_made_on = %(date_made_on)s WHERE id = %(id)s" 
        connectToMySQL(Recipe.database_name).query_db(query,data)
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        print(len(recipe))
        print(recipe)
        # fill all fields
        if len(recipe) < 5 or len(recipe) < 6:
            flash("-All fields must be filled","recipe-error")
            is_valid = False
        if len(recipe["name"]) < 3 or len(recipe["description"]) < 3 or len(recipe["instructions"]) < 3:
            flash("-All fields must be at least 3 characters Long","recipe-error")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_recipe_on_edit(recipe):
        is_valid = True
        print(len(recipe))
        print(recipe)
        # fill all fields
        if  len(recipe) < 6:
            flash("-All fields must be filled","recipe-error")
            is_valid = False
        if len(recipe["name"]) < 3 or len(recipe["description"]) < 3 or len(recipe["instructions"]) < 3:
            flash("-All fields must be at least 3 characters Long","recipe-error")
            is_valid = False
        return is_valid