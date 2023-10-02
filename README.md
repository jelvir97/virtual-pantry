# Virtual Pantry

Link: https://virtual-pantry-elvir.onrender.com/
API: https://www.themealdb.com/api.php

## Description

Virtual Pantry is a pantry manager for keeping track of food items in your pantry! A user can create different pantries for the different locations food is stored in their home, office, or wherever. Virtual pantry also allows a user to save, create, and lookup recipes based off of a singe ingredient.

## Features

- Creation of multiple pantries
- Logging and managing of Ingredients in different pantries.
- Looking up of recipes based off ingredients in pantries.
- Creation of user recipes
- Ability to save recipes suggested by API

## User Flow

Users will be asked to sign up, or log in if an account exists. Once logged in the user is met with a dashboard where they can view or add, pantries and recipes. Adding a recipe will take the user to the recipe view page where they can dynamically add or remove ingredients. From the dashboard users can also save or view recipes that are saved/suggested. Clicking on a recipe will take them to the recipe view page where they will see a list of ingredients and instructions.

## Tech Stack
-Python 3.11.3
    -Flask
    -WTForms
    -SQLAlchemy
-Postgresql
-HTML, CSS, and JavaScript
    -jQuery
    -Bootstrap them from Bootswatch : https://bootswatch.com/sketchy/

## Run Locally

Download zip or clone repository

Create virtual environment and activate:
>`$ python3 -m venv venv`
>`$ source venv/bin/activate`

Install dependencies:
>`$ pip install -r requirements.txt`

Create local postgres DB:
>`$ createdb virtual_pantry`

In app.py set DB URL and secret key:
>`app.config["SQLALCHEMY_DATABASE_URI"] = postgresql:///virtual_pantry`
>`app.config["SECRET_KEY"] = secret_key`

Seed DB:
>`$ ipython`
>`%run seed.py`

Finally, start server:
>`flask run --debug`

## Other Notes
The deployed project is hosted on render.com using a free instance. Free instances spin down with more than 15 minutes of inactivity. Please allow a few minutes for server to restart when using. Thank you!