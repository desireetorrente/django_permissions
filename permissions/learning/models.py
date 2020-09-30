import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Bot(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='img/', blank=True)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (('bot_publish', 'Publica un bot'), )

    def __str__(self):
        return self.name


class Company(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(
        'Company', on_delete=models.SET_NULL, null=True)
    work_position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
