from flask_app import app
# importing all controllers
from flask_app.controllers import users,recipes

if __name__=="__main__":
    app.run(debug=True)