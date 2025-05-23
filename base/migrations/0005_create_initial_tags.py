# Generated by Django 5.1.6 on 2025-04-01 19:04

from django.db import migrations
from django.utils.text import slugify

def create_initial_tags(apps, schema_editor):
    Tag = apps.get_model('base', 'Tag')
    initial_tags = ['Breakfast', 'Lunch', 'Dinner', 'Entree', 'Sides', 'Drinks']
    for tag_name in initial_tags:
        Tag.objects.create(
            name=tag_name,
            slug=slugify(tag_name)
        )

def remove_initial_tags(apps, schema_editor):
    Tag = apps.get_model('base', 'Tag')
    Tag.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_tag_blog_tags'),
    ]

    operations = [
        migrations.RunPython(create_initial_tags, remove_initial_tags),
    ]
