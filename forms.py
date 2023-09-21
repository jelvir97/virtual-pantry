from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from models import db, User, Recipe, Ingredient, Pantry,Category
from wtforms import EmailField, StringField, FloatField, SelectField,FormField,FieldList
from wtforms.validators import DataRequired, Optional

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod 
    def get_session(self):
        return db.session

class LoginForm(ModelForm):
    class Meta:
        model = User
        only = ['email','password']
    
    email = EmailField(validators=[DataRequired()])

class RegisterForm(ModelForm):
    class Meta:
        model = User
        exclude = ['img_url']
    email = EmailField(validators=[DataRequired()])

class PantryForm(ModelForm):
    class Meta:
        model = Pantry

measurement_choices = [
    ('cup','cup'),
    ('fl oz','fl oz'),
    ('mg','mg'),
    ('grams','grams'),
    ('tsp','tsp'),
    ('tbsp','tbsp'),
    ('pint','pint'),
    ('gallon','gallon'),
    ('to taste','to taste'),
    ('dash','dash'),
    ('oz','oz'),
    ('lbs','lbs'),
    ('lbs','lbs')
]
class RecIngForm(FlaskForm):
    ing = StringField('Ingredient:')
    amount = FloatField('Amount:')
    measurement = SelectField('Measurement:', choices=measurement_choices)
    
# cats = [(c.id,c.name) for c in Category.query.all()]   
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['measurements']

    ingredients = FieldList(FormField(RecIngForm), min_entries=1, validators=[Optional()])

