# Generated by Django 4.2.4 on 2023-08-30 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0027_featurecompletetoy_release_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="fullfeaturedsnippet",
            name="some_number",
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
