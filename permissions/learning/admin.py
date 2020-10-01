from django.contrib import admin

from .models import Bot, Company, UserProfile
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from django.contrib import messages


class BotAdmin(GuardedModelAdmin):
    list_display = ('name', 'company', 'created_by' )
    actions = ['make_published']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(request.user, 'learning.view_bot', qs, accept_global_perms=False)

    def make_published(self, request, queryset):
        if request.user.has_perm('learning.bot_publish'):
            updated = get_objects_for_user(request.user, 'learning.bot_publish', queryset)
            print(updated)
            self.message_user(request,
                'Selected bots successfully published.',
                messages.SUCCESS)
        else:
            self.message_user(request,
                f'You are not allowed to perform this action',
                messages.ERROR)

    make_published.short_description = "Publish bot"



class CompanyAdmin(GuardedModelAdmin):
    list_display = ('name', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(request.user, 'learning.view_company', qs, accept_global_perms=False)

# Register your models here.
admin.site.register(Bot, BotAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile)
