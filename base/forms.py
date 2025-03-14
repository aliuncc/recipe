from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Recipe, User, Comment

# Custom User Registration Form (Fixes Email Login Issue)
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'email', 'password1', 'password2']  # Remove username, use email instead

# User Profile Update Form
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'email', 'bio']

# Recipe Creation Form
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'cuisine', 'image']

# Comment Form for Recipes
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
