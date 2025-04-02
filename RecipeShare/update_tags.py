import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django3155.settings')
django.setup()

from base.models import Tag

# Delete all existing tags
Tag.objects.all().delete()

# Create new simplified tag categories
new_tags = [
    'Breakfast',
    'Lunch',
    'Dinner',
    'Entree',
    'Sides',
    'Drink'
]

for tag_name in new_tags:
    Tag.objects.create(name=tag_name) 