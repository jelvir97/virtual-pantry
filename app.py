from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Ingredient, Recipe, Category, Pantry, User
from flask_login import LoginManager

# from forms import RegisterForm, LoginForm, AddFeedbackForm, UpdateFeedbackForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///virtual_pantry'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'mangotreeee'
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def home():
    return 'Welcome'