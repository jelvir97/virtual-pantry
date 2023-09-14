from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from models import db, User, Recipe, Ingredient, Pantry
from wtforms import EmailField
from wtforms.validators import DataRequired

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
    
    

# class RecipeForm(ModelForm):
#     class Meta:
#         model = Recipe