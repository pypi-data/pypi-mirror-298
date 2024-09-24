# Generated by Django 4.0.5 on 2022-07-20 14:52

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0076_modellogentry_revision"),
        ("tests", "0004_eventindex_intro_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="PreviewableModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "categories",
                    modelcluster.fields.ParentalManyToManyField(
                        blank=True, to="tests.eventcategory"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail.models.PreviewableMixin, models.Model),
        ),
        migrations.CreateModel(
            name="NonPreviewableModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "latest_revision",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.revision",
                        verbose_name="latest revision",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail.models.PreviewableMixin, models.Model),
        ),
        migrations.CreateModel(
            name="MultiPreviewModesModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                (
                    "latest_revision",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.revision",
                        verbose_name="latest revision",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail.models.PreviewableMixin, models.Model),
        ),
    ]
