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

    # Allow create superuser
    if not user.is_superuser:
        user_role = user.userprofile.role

        # TODO try the implementation without the statement
        # Anonymous_user because in the settings we set
        # the anonymous user to None.
        if created and user.username != settings.ANONYMOUS_USER_NAME:
            # Global permissions
            if user_role == UserProfile.Role.EDITOR:
                global_permissions_template = Group.objects.get(
                    name="Employee Permissions Template")

            if user_role == UserProfile.Role.ADMIN:
                global_permissions_template = Group.objects.get(
                    name="Admin Permissions Template")

            if user_role == UserProfile.Role.AGENT:
                global_permissions_template = Group.objects.get(
                    name="Agent Permissions Template")

            # Specific permissions
            read_permissions_group, _ = Group.objects.get_or_create(
                name=f"{user.username}: Read")
            write_permissions_group, _ = Group.objects.get_or_create(
                name=f"{user.username}: Write")
            own_permissions_group, _ = Group.objects.get_or_create(
                name=f"{user.username}: Own")

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
