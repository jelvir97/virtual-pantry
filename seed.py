"""Seed database with sample data from API Ingredients List."""

from csv import DictReader
from app import db
from models import Ingredients
import requests


db.drop_all()
db.create_all()


r = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list')
ing = r.json()['meals']

for i in ing:
    ingredient = Ingredients(name=i['strIngredient'])
    db.session.add(ingredient)

db.session.commit() 