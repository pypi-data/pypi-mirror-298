# Generated by Django 4.2.1 on 2023-06-14 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0084_add_default_page_permissions"),
    ]

    # Add a nullable permission ForeignKey and make the old permission_type
    # field nullable so both formats still work for the duration of the
    # deprecation period.
    operations = [
        migrations.AddField(
            model_name="grouppagepermission",
            name="permission",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="auth.permission",
                verbose_name="permission",
            ),
        ),
        migrations.AlterField(
            model_name="grouppagepermission",
            name="permission_type",
            field=models.CharField(
                verbose_name="permission type",
                null=True,
                blank=True,
                max_length=20,
                choices=[
                    ("add", "Add/edit pages you own"),
                    ("bulk_delete", "Delete pages with children"),
                    # Use "change" instead of "edit" to match Django's permission codename
                    ("change", "Edit any page"),
                    ("lock", "Lock/unlock pages you've locked"),
                    ("publish", "Publish any page"),
                    ("unlock", "Unlock any page"),
                ],
            ),
        ),
    ]
