# Generated by Django 4.0.10 on 2023-09-25 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailsearchpromotions", "0006_reset_query_sequence"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchpromotion",
            name="external_link_text",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="searchpromotion",
            name="external_link_url",
            field=models.URLField(
                blank=True,
                help_text="Alternatively, use an external link for this promotion",
                verbose_name="External link URL",
            ),
        ),
        migrations.AlterField(
            model_name="searchpromotion",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Applies to internal page or external link",
                verbose_name="description",
            ),
        ),
        migrations.AlterField(
            model_name="searchpromotion",
            name="page",
            field=models.ForeignKey(
                blank=True,
                help_text="Choose an internal page for this promotion",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="wagtailcore.page",
                verbose_name="page",
            ),
        ),
    ]
