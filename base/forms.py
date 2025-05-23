from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Recipe, User, Comment, Blog

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
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form__input'}),
            'name': forms.TextInput(attrs={'class': 'form__input'}),
            'email': forms.EmailInput(attrs={'class': 'form__input'}),
            'bio': forms.Textarea(attrs={'class': 'form__input', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form__input'}),
        }

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
        fields = ['name', 'description', 'ingredients', 'cuisine', 'image', 'tags']
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
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check'
            })
        }
        labels = {
            'name': 'Recipe Name',
            'description': 'Instructions',
            'ingredients': 'Ingredients List',
            'cuisine': 'Cuisine Type',
            'image': 'Recipe Image',
            'tags': 'Tags'
        }

# Comment Form for Recipes
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

# Blog Form for creating and editing blog posts
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        words = content.split()
        if len(words) < 150:
            raise forms.ValidationError("Blog content must be at least 150 words long.")
        return content

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if not tags:
            raise forms.ValidationError("Please select at least one tag.")
        return tags
