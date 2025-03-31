from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Recipe, User, Comment

# Custom User Registration Form
class MyUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        if commit:
            user.save()
        return user

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
