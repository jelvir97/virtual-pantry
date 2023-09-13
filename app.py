import flask
from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Ingredient, Recipe, Category, Pantry, User
from flask_login import LoginManager,login_required
from forms import LoginForm
from flask_login import login_user

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

        next = flask.request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if not url_has_allowed_host_and_scheme(next, request.host):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)