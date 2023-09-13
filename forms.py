from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from models import db, User, Recipe, Ingredient, Pantry

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod 
    def get_session(self):
        return db.session

class LoginForm(ModelForm):
    class Meta:
        model = User
        only = ['email','password']

class RegisterForm(ModelForm):
    class Meta:
        model = User
    
    

# class RecipeForm(ModelForm):
#     class Meta:
#         model = Recipe