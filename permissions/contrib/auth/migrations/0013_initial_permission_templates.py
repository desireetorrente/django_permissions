# Generated by Django 3.1.1 on 2020-10-04 22:03

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


def create_permission_templates(apps, schema_editor):
    # https://code.djangoproject.com/ticket/23422
    emit_post_migrate_signal(2, False, 'default')

    """Set site domain and name."""
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    
    employee_permissions = Permission.objects.filter(codename__in=[
        'view_bot',
        'add_bot',
        'change_bot',
        'delete_bot',
        'view_company',
        'view_user',
        'change_user',
        'view_userprofile',
        'change_userprofile'
    ])

    employee_permission_template = Group.objects.create(name="Employee Permissions Template")
    employee_permission_template.permissions.set(employee_permissions)

    admin_permissions = Permission.objects.filter(codename__in=[
        'view_bot',
        'add_bot',
        'change_bot',
        'delete_bot',
        'view_company',
        'change_company',
        'view_user',
        'add_user',
        'change_user',
        'delete_user',
        'view_userprofile',
        'add_userprofile',
        'change_userprofile'
    ])

    admin_permission_template = Group.objects.create(name="Admin Permissions Template")
    admin_permission_template.permissions.set(admin_permissions)

    agent_permissions = Permission.objects.filter(codename__in=[
        'view_bot',
        'add_bot',
        'change_bot',
        'delete_bot',
        'view_company',
        'add_company',
        'change_company',
        'delete_company',
        'view_user',
        'add_user',
        'change_user',
        'delete_user',
        'view_userprofile',
        'add_userprofile',
        'change_userprofile'
    ])

    agent_permission_template = Group.objects.create(name="Agent Permissions Template")
    agent_permission_template.permissions.set(agent_permissions)


def remove_permission_templates(apps, schema_editor):
    """Revert site domain and name to default."""
    Group = apps.get_model("auth", "Group")

    employees_group = Group.objects.get(name=f"Employee Permissions Template")
    employees_group.delete()

    admin_group = Group.objects.get(name=f"Admin Permissions Template")
    admin_group.delete()

    agent_group = Group.objects.get(name=f"Agent Permissions Template")
    agent_group.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [migrations.RunPython(create_permission_templates, remove_permission_templates)]
