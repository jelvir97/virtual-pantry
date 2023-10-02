import flask
import os
from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect,url_for,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Ingredient, Recipe, Category, Pantry, User
from flask_login import LoginManager,login_required, login_user,logout_user, current_user
from forms import LoginForm, RegisterForm, PantryForm, RecipeForm, UserUpdateForm
import requests
from  sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# retrieves user obj for views.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@login_required
def home():
    """Renders home dashboard"""
    try:
        rec = rand_recipe()
    except:
        db.session.rollback()
        rec = Recipe.query.order_by(func.random()).first()
    return render_template('home.html',rec=rec)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """logs in user"""
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    print(app.config['SECRET_KEY'])
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(email=form.data['email'],pwd=form.data['password'])
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        next = flask.request.args.get('next')

        flask.flash('Logged in successfully.')

        return flask.redirect(next or url_for('home'))
    return flask.render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    """Registers new user and adds them to db"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    print(form['csrf_token'])
    if form.validate_on_submit():
        try:
            user = User.register(first_name=form.data['first_name'],
                                last_name=form.data['last_name'],
                                email=form.data['email'],
                                password=form.data['password'])
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append('There is already an account with this email!')
            return render_template('signup.html',form=form)
        else:

            login_user(user)
        flash('Signed Up Successfully.')

        return redirect(url_for('home'))
    print(form['csrf_token'])
    return render_template('signup.html',form=form)
    
@app.route('/profile')
@login_required
def user_profile():
    return render_template('user_profile.html')

@app.route('/profile/update',methods=['GET'])
@login_required
def user_profile_update():
    form = UserUpdateForm(obj=current_user)
    return render_template('user_update.html',form=form)

@app.route('/profile/update',methods=['POST'])
@login_required
def submit_user_update():
    form = UserUpdateForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        return redirect(url_for('user_profile'))
    return redirect(url_for('user_profile_update'))

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('signup'))

# 
# Pantry - Ingredient Views
# 
@app.route('/pantry/new', methods=['GET','POST'])
@login_required
def new_pantry():
    """adding new pantry form"""
    form = PantryForm()
    if form.validate_on_submit():
        p = Pantry(name=form.data['name'],type=form.data['type'],user_id=int(current_user.id))
        db.session.add(p)
        db.session.commit() 
        return redirect(url_for('view_pantry',p_id=p.id))
        
    return render_template('new_pantry.html', form = form)


@app.route('/pantry/<int:p_id>')
@login_required
def view_pantry(p_id):
    pantry = Pantry.query.get(p_id)
    return render_template('pantry.html',pantry=pantry)

@app.route('/ingredient/search/<q>')
def search_ing(q):
    search = "%{}%".format(q)
    ings = Ingredient.query.filter(Ingredient.name.ilike(search)).limit(5)
    results = [ing.name for ing in ings]
    return jsonify(results)

@app.route('/pantry/<int:p_id>/ingredient/<name>')
def add_ing(p_id,name):
    ing = Ingredient.query.filter_by(name=name).one()
    p =Pantry.query.get(p_id)
    p.ingredients.append(ing)
    db.session.commit()
    return redirect(url_for('view_pantry',p_id=p_id))

@app.route('/pantry/<int:id>/ingredient')
def list_ingredients(id):
    p = Pantry.query.get(id)
    return p.ingredients_json()

@app.route('/pantry/<int:p_id>/ingredient/<int:i_id>/remove', methods=["POST"])
def pantry_ingredient_remove(p_id,i_id):
    p =  Pantry.query.get(p_id)
    i = Ingredient.query.get(i_id)
    p.ingredients.remove(i)
    db.session.commit()
    return redirect(url_for('view_pantry',p_id=p_id))


# Recipe Helper functions
def rand_recipe():
    resp = requests.get('https://www.themealdb.com/api/json/v1/1/random.php?')
    m = resp.json()['meals'][0]
    r = Recipe.add_from_api(m)
    return r

def recipes_by_ing(ing):
    resp = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ing}')
    meals = resp.json()['meals']
    return meals

def recipe_by_id(id):
    resp = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}')
    m = resp.json()['meals'][0]
    r = Recipe.add_from_api(m)
    return r
# 
# Recipe Views
# 

@app.route('/recipe/<int:id>')
@login_required
def view_recipe(id):
    """Renders view page for single recipe"""
    r = Recipe.query.get(id)
    cat = Category.query.get(r.category)
    return render_template('recipe.html',rec=r,cat=cat)

@app.route('/recipe/<int:id>/add', methods=['POST'])
def save_recipe(id):
    """Post method to add recipe to user's saved_recipes"""
    r = Recipe.query.get(id)
    current_user.saved_recipes.append(r)
    db.session.commit()
    flash('Recipe saved!')
    return redirect(url_for('view_recipe',id=r.id)) 

@app.route('/recipe/<int:id>/remove', methods=['POST'])
def unsave_recipe(id):
    """Removing recipes from user's saved_recipes"""
    r = Recipe.query.get(id)
    current_user.saved_recipes.remove(r)
    db.session.commit()
    flash('Recipe unsaved!')
    return redirect(url_for('view_recipe',id=r.id)) 

@app.route('/recipe/new',methods=['GET','POST'])
def new_user_recipe():
    """Renders/Handles new recipe form"""
    form = RecipeForm()
    if form.validate_on_submit():
        print(form)
        rec = Recipe.add_user_recipe(form.data)
        current_user.saved_recipes.append(rec)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_recipe.html',form=form)

@app.route('/recipe/search/<ing>')
@login_required
def recipe_search(ing):
    recipes = recipes_by_ing(ing)
    return render_template('list_recipes.html',recipes=recipes,ing=ing)

@app.route('/recipe/search/api/<int:id>')
@login_required
def recipe_search_id(id):
    rec = recipe_by_id(id)
    return redirect(url_for('view_recipe',id=rec.id))