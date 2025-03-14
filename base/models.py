from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


# Recipe Model
class Recipe(models.Model):
    CUISINE_CHOICES = [
        ('Italian', 'Italian'),
        ('Mexican', 'Mexican'),
        ('Indian', 'Indian'),
        ('Chinese', 'Chinese'),
        ('American', 'American'),
        ('French', 'French'),
        ('Japanese', 'Japanese'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Recipe creator
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()  # List ingredients as comma-separated text
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES, default="Other")
    image = models.ImageField(upload_to="recipes/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Comment Model for Recipe
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Comment author
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Show newest comments first

    def __str__(self):
        return self.body[:50]  # Show first 50 characters of comment
