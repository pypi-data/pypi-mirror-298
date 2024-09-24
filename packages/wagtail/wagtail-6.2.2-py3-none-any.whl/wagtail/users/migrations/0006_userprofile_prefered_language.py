# Generated by Django 1.10.5 on 2017-01-27 22:18
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailusers", "0005_make_related_name_wagtail_specific"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="preferred_language",
            field=models.CharField(
                default="",
                help_text="Select language for the admin",
                max_length=10,
                verbose_name="preferred language",
            ),
        ),
    ]
