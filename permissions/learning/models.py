import uuid

from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase
from guardian.shortcuts import assign_perm

from silk.profiling.profiler import silk_profile

from treenode.models import TreeNodeModel


class User(AbstractUser):

    class Role(models.TextChoices):
        EDITOR = 'ED', _('Editor')
        ADMIN = 'AD', _('Admin')
        AGENT = 'AG', _('Agent')

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        related_name='users'
    )
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.EDITOR,
    )
    work_position = models.CharField(max_length=100, blank=True)

    def grant_permissions(self, user):
        if user.has_perm('learning.view_user'):
            read_permissions = Group.objects.get(name=f"{self.username}: Read")
            user.groups.add(read_permissions)

        if user.has_perm('learning.change_user') and \
                user.has_perm('learning.delete_user'):
            write_permissions = Group.objects.get(name=f"{self.username}: Write")
            user.groups.add(write_permissions)

    def grant_company_permissions(self):
        if self.has_perm('learning.view_company'):
            read_permissions = Group.objects.get(name=f"{self.company.name}: Read")
            self.groups.add(read_permissions)

        if self.has_perm('learning.change_company') and not \
                self.has_perm('learning.delete_company'):
            own_permissions = Group.objects.get(name=f"{self.company.name}: Own")
            self.groups.add(own_permissions)

    def bulk_grant_permissions(self, template, users):
        # Grant permissions to a queryset of users
        with silk_profile(name='ADD resources to user'):

            if template == 'Admin Permissions Template':
                groups = Group.objects.filter(
                    user__in=users).exclude(name__contains='Template')
                self.groups.add(*groups)

                # -----------------
                # Allow the existing users to access this user instance
                read_permissions = Group.objects.get(
                    name=f"{self.username}: Read")
                read_permissions.user_set.add(*users)


        if template == 'Agent Permissions Template':
            read_permissions.user_set.add(*users)
            write_permissions.user_set.add(*users)
            write_permissions.user_set.add(*users)

        if template == 'Employee Permissions Template':
            read_permissions.user_set.add(*users)
            write_permissions.user_set.add(*users)


# Create your models here.
class Bot(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='img/', blank=True)
    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, null=True, related_name='bots')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (('publish_bot', 'Can publish a bot'), )

    def __str__(self):
        return self.name


class Company(TreeNodeModel):
    # the field used to display the model instance
    # default value 'pk'
    treenode_display_field = 'name'

    class Type(models.TextChoices):
        AGENCY = 'AG', _('Agencia')
        REGULAR_COMPANY = 'RC', _('Regular company')
        BOTXO = 'BX', _('Botxo')

    type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.REGULAR_COMPANY,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    name = models.CharField(max_length=200)

    def grant_permissions(self, user):
        if user.has_perm('learning.view_company'):
            read_permissions = Group.objects.get(name=f"{self.name}: Read")
            user.groups.add(read_permissions)

        if user.has_perm('learning.change_company') and \
                user.has_perm('learning.delete_company'):
            write_permissions = Group.objects.get(name=f"{self.name}: Write")
            user.groups.add(write_permissions)

        if user.has_perm('learning.change_company') and not \
                user.has_perm('learning.delete_company'):
            own_permissions = Group.objects.get(name=f"{self.name}: Own")
            user.groups.add(own_permissions)

    # def bulk_grant_permissions(self, template, users):
    #     # Grant permissions to a queryset of users

    #     read_permissions = Group.objects.get(name=f"{self.name}: Read")
    #     write_permissions = Group.objects.get(name=f"{self.name}: Write")

    #     if template == 'Admin Permissions Template':
    #         execute_permissions = Group.objects.get(
    #             name=f"{self.name}: Execute")
    #         execute_permissions.user_set.add(*users)
    #         read_permissions.user_set.add(*users)
    #         write_permissions.user_set.add(*users)

    #     if template == 'Agent Permissions Template':
    #         read_permissions.user_set.add(*users)
    #         write_permissions.user_set.add(*users)

    #     if template == 'Employee Permissions Template':
    #         read_permissions.user_set.add(*users)
    #         write_permissions.user_set.add(*users)

    class Meta(TreeNodeModel.Meta):
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return self.name


# Direct FK for Company model
class CompanyUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Company, on_delete=models.CASCADE)


class CompanyGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Company, on_delete=models.CASCADE)


# Admin performance
from django.core.paginator import Paginator
# with a lot of result we don't need count because we, probably, 
# use some filters.


class NoCountPaginator(Paginator):
    @property
    def count(self):
        return 999999999  # Some arbitrarily large number,
        # so we can still get our page tab.
