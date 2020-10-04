import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        'Company', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (('bot_publish', 'Publica un bot'), )

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    name = name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    class Role(models.TextChoices):
        EDITOR = 'ED', _('Editor')
        ADMIN = 'AD', _('Admin')
        AGENT = 'AG', _('Agent')

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.EDITOR,
    )
    work_position = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.user.username
