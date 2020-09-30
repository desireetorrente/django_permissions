from django.contrib import admin

from .models import Bot, Company, UserProfile
from guardian.admin import GuardedModelAdmin


class BotAdmin(GuardedModelAdmin):
    list_display = ('name', )

class CompanyAdmin(GuardedModelAdmin):
    list_display = ('name', )

# Register your models here.
admin.site.register(Bot, BotAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile)
