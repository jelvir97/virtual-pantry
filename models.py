"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
# from psycopg2.errors import UniqueViolation
# from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

# for helper function: API meal to DB meal h
# measurements = [ m[k] for k in m.keys() if 'strMeasure' in k and m[k] != ' ']

# ings = [ m[k] for k in m.keys() if 'strIngredient' in k and m[k]]

class Ingredient(db.Model):
    """Ingredients used in api Recipes"""

    __tablename__ = "ingredients"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(50),
                     nullable=False)
    
class Recipe(db.Model):
    """Recipes"""

    __tablename__= "recipes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(50),
                     nullable=False)
    
    image = db.Column(db.String())

    instructions= db.Column(db.Text(),
                            nullable=False)
    
    measurements= db.Column(db.ARRAY(db.String(20)))

    ingredients = db.relationship('Ingredient',
                                  secondary='ingredient_recipe', 
                                  backref='recipes')
    
    category = db.Column(db.Integer,
                         db.ForeignKey('categories.id'),
                         nullable=False)

class IngredientRecipe(db.Model):
    """Many-to-many relationship between ingredients and recipes"""

    __tablename__= "ingredient_recipe"

    recipe_id = db.Column(db.Integer,
                        db.ForeignKey('recipes.id'),
                        primary_key=True)

    ingredient_id = db.Column(db.Integer,
                       db.ForeignKey('ingredients.id'),
                       primary_key=True)

class Category(db.Model):
    """Categories for recipes"""

    __tablename__ = "categories"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(20),
                     nullable=False)
    
    recipes = db.relationship('Recipe', backref='categories')
    
class Pantry(db.Model):
    """Pantry model for organizing ingredients"""

    __tablename__= "pantries"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(20),
                     nullable=False)
    
    type = db.Column(db.String(20),
                     nullable=False)
    
    ingredients =db.relationship('Ingredient',
                                  secondary='ingredient_pantry', 
                                  backref='pantries')
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    def add_ingredients(slf, *args):
        for id in args:
            i = Ingredient.query.get(int(i))
            slf.ingredients.append(i)
        db.session.commit

    
class IngredientPantry(db.Model):
    """Many-to-many relation between ingredients and pantries"""

    __tablename__ = 'ingredient_pantry'
    
    ingredient_id = db.Column(db.Integer,
                        db.ForeignKey('ingredients.id'),
                        primary_key=True)
    
    pantry_id = db.Column(db.Integer,
                        db.ForeignKey('pantries.id'),
                        primary_key=True)
    
class User(db.Model, UserMixin):
    """User class fro login and auth"""

    __tablename__ = 'users'

    def __repr__(self):
        return f"<User first_name = {self.first_name} last_name={self.last_name}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                     nullable=False)
    
    last_name = db.Column(db.String(50),
                     nullable=False)
    
    email = db.Column(db.String(100),
                      nullable=False,
                      unique=True)
    
    password = db.Column(db.String(100),
                         nullable=False)
    
    img_url = db.Column(db.String(),
                     nullable=False,
                     default='https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png')
    
    pantries = db.relationship('Pantry',cascade="all, delete-orphan", backref='user')

    @classmethod
    def register(cls, f_name, l_name, email, password):
        """Register user w/hashed password & return user."""

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            new_user = User(first_name=f_name, 
                            last_name=l_name, 
                            email=email, 
                            password=pw_hash)
        except:
            return False
        else:
            return new_user
        
    @classmethod
    def authenticate(cls, email, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(email=email).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
