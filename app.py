import flask
from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect,url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Ingredient, Recipe, Category, Pantry, User
from flask_login import LoginManager,login_required
from forms import LoginForm, RegisterForm
from flask_login import login_user


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
login_manager.login_view = "login"

# retrieves user obj for views.
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@login_required
def home():
    return 'Welcome'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(email=form.data.email,password=form.data.password)
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        return flask.redirect(url_for('home'))
    return flask.render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    """Registers new user and adds them to db"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Signed Up Successfully.')

        return redirect(url_for('home'))

    return render_template('signup.html',form=form)
    
