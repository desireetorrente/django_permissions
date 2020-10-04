from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import Group

from guardian.shortcuts import assign_perm

from .models import UserProfile


@receiver(post_save, sender=get_user_model())
def user_post_save(sender, **kwargs):
    """
    Create all permission groups for the new created user: Read, Write, Own.
    """
    user, created = kwargs["instance"], kwargs["created"]

    if not user.is_superuser:
        user_role = user.userprofile.role

        if created and user.username != settings.ANONYMOUS_USER_NAME:
            # Global permissions
            if user_role == UserProfile.Role.EDITOR:
                global_permissions_template = Group.objects.get(name=f"Employee Permissions Template")
                # global_permissions = Permission.objects.filter(codename__in=[
                #     'view_bot',
                #     'add_bot',
                #     'change_bot',
                #     'delete_bot',
                #     'view_company',
                #     'view_user',
                #     'change_user',
                # ])
            
            if user_role == UserProfile.Role.ADMIN:
                global_permissions_template = Group.objects.get(name=f"Admin Permissions Template")
                # global_permissions = Permission.objects.filter(codename__in=[
                #     'view_bot',
                #     'add_bot',
                #     'change_bot',
                #     'delete_bot',
                #     'view_company',
                #     'change_company',
                #     'view_user',
                #     'add_user',
                #     'change_user',
                #     'delete_user',
                # ])

            if user_role == UserProfile.Role.AGENT:
                global_permissions_template = Group.objects.get(name=f"Agent Permissions Template")
                # global_permissions = Permission.objects.filter(codename__in=[
                #     'view_bot',
                #     'add_bot',
                #     'change_bot',
                #     'delete_bot',
                #     'view_company',
                #     'add_company',
                #     'change_company',
                #     'delete_company',
                #     'view_user',
                #     'add_user',
                #     'change_user',
                #     'delete_user',
                # ])

            # Specific permissions
            read_permissions_group, _ = Group.objects.get_or_create(name=f"{user.username}: Read")
            write_permissions_group, _ = Group.objects.get_or_create(name=f"{user.username}: Write")
            own_permissions_group, _ = Group.objects.get_or_create(name=f"{user.username}: Own")
            
            # Read
            assign_perm('view_user', read_permissions_group, user)

            # Write
            assign_perm('change_user', write_permissions_group, user)
            assign_perm('delete_user', write_permissions_group, user)

            # Own
            assign_perm('change_user', own_permissions_group, user)

            user.groups.add(global_permissions_template)
            user.groups.add(read_permissions_group)
            user.groups.add(own_permissions_group)


@receiver(post_delete, sender=get_user_model())
def user_post_delete(sender, **kwargs):
    """
    Delete all permission groups for the deleted user: Read, Write, Own.
    """
    user = kwargs["instance"]

    if user.username != settings.ANONYMOUS_USER_NAME:
        try:
            read_permissions_group = Group.objects.get(
                name=f"{user.username}: Read")
            read_permissions_group.delete()
        except Group.DoesNotExist:
            pass

        try:
            write_permissions_group = Group.objects.get(
                name=f"{user.username}: Write")
            write_permissions_group.delete()
        except Group.DoesNotExist:
            pass

        try:
            own_permissions_group = Group.objects.get(
                name=f"{user.username}: Own")
            own_permissions_group.delete()
        except Group.DoesNotExist:
            pass
