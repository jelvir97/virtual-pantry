"""View function tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Ingredient, Recipe, Category, Pantry, IngredientPantry,IngredientRecipe
from sqlalchemy.exc import IntegrityError
import seed

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///pantry-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

class ModelTestCase(TestCase):
    """Testing User, Recipe, and Ingredient Models"""
    

    def setUp(self):
        """Clearing db for tests"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        db.session.rollback()
        IngredientPantry.query.delete()
        IngredientRecipe.query.delete()
        Ingredient.query.delete()
        Pantry.query.delete()
        User.query.delete()
        Recipe.query.delete()
        Category.query.delete()

        self.client = app.test_client()

        self.testuser = User.register(
            email="test@test.com",
            first_name="test",
            last_name="user",
            password="HASHED_PASSWORD"
        )
        db.session.add(self.testuser)
        db.session.commit()

        seed.seed_test_db()

    def test_user_signup(self):
        """Test User Signup"""
        with self.client as c:
            resp = c.post('/signup', data={'email':"test2@test2.com",
                'first_name':"test2",
                'last_name':"user2",
                'password':"HASHED_PASSWORD"},
                follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Pantries",resp.text)


