from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)  # Followers

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def followers_count(self):
        return self.followers.count()  # Count of followers

    def following_count(self):
        return self.following.count()  # Count of users this user follows


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
    likes = models.ManyToManyField(User, related_name="recipe_likes", blank=True)  # Likes

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()  # Count of likes on this recipe


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
