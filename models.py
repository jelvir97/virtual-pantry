"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# for helper function: API meal to DB meal h
# measurements = [ m[k] for k in m.keys() if 'strMeasure' in k and m[k] != ' ']

# ings = [ m[k] for k in m.keys() if 'strIngredient' in k and m[k]]

class Ingredients(db.Model):
    """Ingredients used in api Recipes"""

    __tablename__ = "ingredients"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(50),
                     nullable=False)