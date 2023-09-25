"""Models tests."""

# run these tests like:
#
#    python -m unittest test_models.py


import os
from unittest import TestCase

from models import db, User, Ingredient, Recipe, Category, Pantry
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///pantry-test"


# Now we can import app

from app import app
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///pantry-test'
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

class ModelTestCase(TestCase):
    """Testing User, Recipe, and Ingredient Models"""

    def setUp(self):
        """Clearing db for tests"""
        db.session.rollback()
        User.query.delete()
        Ingredient.query.delete()
        Recipe.query.delete()
        Category.query.delete()
        Pantry.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Testing instantiation of User model"""

        u = User(
            email="test@test.com",
            first_name="test",
            last_name="user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(User.query.all()),1)
        self.assertEqual(u.email, "test@test.com")

    def test_user_registration(self):
        u = User.register(
            email="test@test.com",
            first_name="test",
            last_name="user",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertNotEqual(u.password,"HASHED_PASSWORD")
        self.assertEqual(len(User.query.all()),1)
        self.assertEqual(u.first_name,'test')

    def test_recipe_model(self):
        c = Category(name='testCat')
        db.session.add(c)
        db.session.commit()

        r = Recipe(name='testRec',
                   instructions='test test test',
                   category=c.id,
                   measurements=['test','test','test'])
        db.session.add(r)
        db.session.commit()

        self.assertEqual(len(Recipe.query.all()),1)
        self.assertEqual(r.category,c.id)

    def test_ingredients_model(self):
        ing1 = Ingredient(name='salt')
        ing2 = Ingredient(name='pepper')
        ing3 = Ingredient(name='eggs')

        db.session.add(ing1)
        db.session.add(ing2)
        db.session.add(ing3)
        db.session.commit()

        self.assertEqual(len(Ingredient.query.all()),3)
    
