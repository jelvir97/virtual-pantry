"""View function tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Ingredient, Recipe
from sqlalchemy.exc import IntegrityError

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


db.create_all()

class ModelTestCase(TestCase):
    """Testing User, Recipe, and Ingredient Models"""

    def setUp(self):
        """Clearing db for tests"""
        db.session.rollback()
        User.query.delete()
        Ingredient.query.delete()
        Recipe.query.delete()

        self.client = app.test_client()

 