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
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'placeholder': 'Enter each ingredient on a new line, for example:\n2 cups flour\n1 cup sugar\n3 eggs'
        }),
        help_text='Enter each ingredient on a new line'
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Describe your recipe, including preparation steps...'
        })
    )
    
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'cuisine', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter recipe name',
                'class': 'form-control'
            }),
            'cuisine': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Recipe Name',
            'description': 'Instructions',
            'ingredients': 'Ingredients List',
            'cuisine': 'Cuisine Type',
            'image': 'Recipe Image'
        }

# Comment Form for Recipes
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
