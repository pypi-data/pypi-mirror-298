# Generated by Django 3.1.8 on 2021-06-22 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailsearchpromotions", "0003_query_querydailyhits"),
    ]

    # Changed to a no-op in Wagtail 6.0.
    # This migration previously copied the contents of the Query table from wagtailsearch to
    # wagtailsearchpromotions; however, this can't be done after wagtailsearch migration 0008,
    # which removes the Query table (and we can't force it to run before, because the
    # searchpromotions app can be installed at any time). However, any project that needs this
    # data migration would have already applied the real version of this migration while they
    # were running Wagtail 5.
    operations = []
