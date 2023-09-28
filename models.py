"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy_utils import EmailType, URLType
from wtforms import PasswordField, RadioField
import sqlalchemy
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
    
    def serialize(self):
        d = {'id':self.id,
             'name' :self.name}
        return d
    
class Recipe(db.Model):
    """Recipes"""

    __tablename__= "recipes"

    def __repr__(slf):
        return f"<R: {slf.name} {slf.id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(),
                     nullable=False,
                     info={'label': 'Recipe Name'})
    
    image = db.Column(db.String(),
                      info={'label': 'Recipe Image'})

    instructions= db.Column(db.Text(),
                            nullable=False,
                            info={'label': 'Instructions'})
    
    measurements= db.Column(db.ARRAY(db.String()))

    ingredients = db.relationship('Ingredient',
                                  secondary='ingredient_recipe', 
                                  backref='recipes')
    
    category = db.Column(db.Integer,
                         db.ForeignKey('categories.id'),
                         nullable=False,
                         info={'label': 'Category',
                               'choices': [(1,'Beef'),
                                           (2,'Breakfast'),
                                           (3,'Chicken'),
                                           (4,'Dessert'),
                                           (5,'Goat'),
                                           (6,'Lamb'),
                                           (7,'Misc'),
                                           (8,'Pasta'),
                                           (9,'Pork'),
                                           (10,'Seafood'),
                                           (11,'Side'),
                                           (12,'Starter'),
                                           (13,'Vegan'),
                                           (14,'Vegetarian')]})
    
    @classmethod
    def add_from_api(cls, m):
        """Receives meal data from api and adds as Recipe to db"""
        measurements = [ m[k] for k in m.keys() if 'strMeasure' in k and m[k] != ' ']
        ings = [ m[k] for k in m.keys() if 'strIngredient' in k and m[k]]
        cat = Category.query.filter_by(name=m['strCategory']).one()
        newRec = cls(name=m['strMeal'], image=m['strMealThumb'], instructions=m['strInstructions'],measurements=cls.ingredient_list(measurements,ings),category=cat.id)
        db.session.add(newRec)
        db.session.commit()

        newRec.add_ingredients(ings)

        return newRec
    
    def add_ingredients(slf, ings):
        for ing in ings:
            try:
                i = Ingredient.query.filter_by(name=ing).one()

            except sqlalchemy.exc.NoResultFound:
                i = Ingredient(name=ing)
                db.session.add(i)
                db.session.commit()

            slf.ingredients.append(i)
        db.session.commit()

    @classmethod
    def ingredient_list(cls,ms,ings):
        """Makes list of concatenated ingredient/measurement pairs"""

        i_m_list = [ings[x] + ' ' + ms[x] for x in range(0,len(ings))]

        return i_m_list
    
    @classmethod
    def add_user_recipe(cls, data):
        name = data['name']
        instructions = data['instructions']
        image = data['image']
        category= int(data['category'])
        ings = []
        ms = []
        for i in data['ingredients']:
            if i['ing']:
                ms.append(str(i['amount']) + ' ' + i['measurement'])
                ings.append(i['ing'].capitalize())
        
        measurements = cls.ingredient_list(ms,ings)

        newRec = cls(name=name,instructions=instructions,image=image,measurements=measurements,category=category)
        db.session.add(newRec)
        db.session.commit()

        newRec.add_ingredients(ings)

        return newRec
        
        

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
                     nullable=False,
                     info={'label': 'Pantry Name'})
    
    type = db.Column(db.String(20),
                     nullable=False,
                     info={'label': 'Type',
                           'form_field_class': RadioField,
                            'choices':[('pantry','Pantry'),('fridge','Fridge'),('freezer','Freezer')]})
    
    ingredients =db.relationship('Ingredient',
                                  secondary='ingredient_pantry', 
                                  backref='pantries')
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    def add_ingredients(slf, *args):
        """takes variable arguments for appending to pantry.ingredients"""
        for id in args:
            i = Ingredient.query.get(int(id))
            slf.ingredients.append(i)
        db.session.commit

    def ingredients_json(self):
        ings = self.ingredients

        d = {}
        for i in ings:
            d.update({i.name:i.serialize()})
        return d


    
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
                   autoincrement=True,
                   )
    
    first_name = db.Column(db.String(50),
                     nullable=False,
                     info={'label': 'First Name'})
    
    last_name = db.Column(db.String(50),
                     nullable=False,
                     info={'label': 'Last Name'})
    
    email = db.Column(EmailType,
                      nullable=False,
                      unique=True,
                      info={'label': 'Email'})
    
    password = db.Column(db.String(),
                         nullable=False,
                         info={'form_field_class': PasswordField,
                               'label':'Password'})
    
    img_url = db.Column(URLType,
                     nullable=False,
                     default='https://www.tenforums.com/geek/gars/images/2/types/thumb_15951118880user.png',
                     info={'label': 'Profile Picture'})
    
    pantries = db.relationship('Pantry',cascade="all, delete-orphan", backref='user')

    saved_recipes = db.relationship('Recipe', secondary='user_recipe',backref='user')

    @classmethod
    def register(cls, first_name, last_name, email, password):
        """Register user w/hashed password & return user."""

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            new_user = User(first_name=first_name, 
                            last_name=last_name, 
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

class UserRecipe(db.Model):
    """Many to many relationship between recipes and user"""
    __tablename__ = 'user_recipe'
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    
    recipe_id = db.Column(db.Integer,
                        db.ForeignKey('recipes.id'),
                        primary_key=True)