"""Seed database with sample data from API Ingredients List."""

from csv import DictReader
from app import db
from models import Ingredient, Category
import requests


db.drop_all()
db.create_all()


r = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list')
ing = r.json()['meals']

for i in ing:
    ingredient = Ingredient(name=i['strIngredient'])
    db.session.add(ingredient)

r2 = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list')
cats = r2.json()['meals']

for cat in cats:
    category = Category(name=cat['strCategory'])
    db.session.add(category)

db.session.commit() 