# Generated by Django 2.0.4 on 2018-05-04 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtaildocs", "0007_merge"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="file_size",
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
    ]
