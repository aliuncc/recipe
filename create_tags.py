import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django3155.settings')
django.setup()

from base.models import Tag

tags = [
    'Vegetarian',
    'Vegan',
    'Gluten-Free',
    'Quick & Easy',
    'Dessert',
    'Breakfast',
    'Lunch',
    'Dinner',
    'Snack',
    'Healthy'
]

for tag_name in tags:
    Tag.objects.get_or_create(name=tag_name) 