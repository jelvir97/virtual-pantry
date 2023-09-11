"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    
    category = db.relationship('Category', backref='recipes')

class IngredientRecipe(db.Model):
    """Many-to-many relationship between ingredients and recipes"""

    __tablename__= "ingredient_recipe"

    recipe_id = db.Column(db.Integer,
                        db.ForeignKey('recipes.id'),
                        primary_key=True)

    ingredient_id = db.Column(db.Integer,
                       db.ForeignKey('ingredients.id'),
                       primary_key=True)

class Catgeory(db.Model):
    """Categories for recipes"""

    __tablename__ = "categories"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(20),
                     nullable=False)
