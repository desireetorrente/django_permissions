from django.contrib import admin

from .models import Bot, Company, UserProfile

# Register your models here.
admin.site.register(Bot)
admin.site.register(Company)
admin.site.register(UserProfile)
