# Generated by Django 4.2b1 on 2023-03-21 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("snippetstests", "0009_filterablesnippet_some_date"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FilterableSnippet",
        ),
    ]
