# Generated by Django 3.1.2 on 2020-10-13 22:43

from django.db import migrations


def add_choose_permission_to_admin_groups(apps, _schema_editor):
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    Group = apps.get_model("auth.Group")

    # Get image content type
    image_content_type, _created = ContentType.objects.get_or_create(
        model="image", app_label="wagtailimages"
    )

    # Create the Choose permission (if it doesn't already exist)
    choose_image_permission, _created = Permission.objects.get_or_create(
        content_type=image_content_type,
        codename="choose_image",
        defaults={"name": "Can choose image"},
    )

    # Assign it to all groups which have "Access the Wagtail admin" permission.
    # This emulates the previous behaviour, where everyone could choose any image in any Collection
    # because choosing wasn't permissioned.
    for group in Group.objects.filter(permissions__codename="access_admin"):
        group.permissions.add(choose_image_permission)


def remove_choose_permission(apps, _schema_editor):
    """Reverse the above additions of permissions."""
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    image_content_type = ContentType.objects.get(
        model="image",
        app_label="wagtailimages",
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=image_content_type, codename="choose_image"
    ).delete()


def get_choose_permission(apps):
    Permission = apps.get_model("auth.Permission")
    ContentType = apps.get_model("contenttypes.ContentType")

    image_content_type, _created = ContentType.objects.get_or_create(
        model="image",
        app_label="wagtailimages",
    )
    return Permission.objects.filter(
        content_type=image_content_type, codename__in=["choose_image"]
    ).first()


def copy_choose_permission_to_collections(apps, _schema_editor):
    Collection = apps.get_model("wagtailcore.Collection")
    Group = apps.get_model("auth.Group")
    GroupCollectionPermission = apps.get_model("wagtailcore.GroupCollectionPermission")

    root_collection = Collection.objects.get(depth=1)

    permission = get_choose_permission(apps)
    if permission:
        for group in Group.objects.filter(permissions=permission):
            GroupCollectionPermission.objects.create(
                group=group, collection=root_collection, permission=permission
            )


def remove_choose_permission_from_collections(apps, _schema_editor):
    GroupCollectionPermission = apps.get_model("wagtailcore.GroupCollectionPermission")
    choose_permission = get_choose_permission(apps)
    if choose_permission:
        GroupCollectionPermission.objects.filter(permission=choose_permission).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0022_uploadedimage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="image",
            options={
                "permissions": [("choose_image", "Can choose image")],
                "verbose_name": "image",
                "verbose_name_plural": "images",
            },
        ),
        migrations.RunPython(
            add_choose_permission_to_admin_groups, remove_choose_permission
        ),
        migrations.RunPython(
            copy_choose_permission_to_collections,
            remove_choose_permission_from_collections,
        ),
    ]
