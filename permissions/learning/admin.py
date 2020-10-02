from django.contrib import admin

from .models import Bot, Company, UserProfile
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from django.contrib import messages


class BotAdmin(GuardedModelAdmin):
    list_display = ('name', 'company', 'created_by')
    actions = ['make_published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'learning.view_bot', qs,
            accept_global_perms=False)

    def make_published(self, request, queryset):
        if request.user.has_perm('learning.bot_publish'):
            updated = get_objects_for_user(
                request.user, 'learning.bot_publish',
                queryset)
            print(updated)
            self.message_user(
                request,
                'Selected bots successfully published.',
                messages.SUCCESS)
        else:
            self.message_user(
                request,
                'You are not allowed to perform this action',
                messages.ERROR)

    make_published.short_description = "Publish bot"


class BotsInline(admin.TabularInline):
    model = Bot


class CompanyAdmin(GuardedModelAdmin):
    list_display = ('name', 'created_by')
    inlines = [
        BotsInline,
    ]

    def save_model(self, request, obj, form, change):
        qs = super().get_queryset(request)
        user_instance_permissions = get_objects_for_user(
            request.user, 'learning.change_company', qs,
            accept_global_perms=False)
        print('test get user objects', user_instance_permissions)
        if user_instance_permissions:
            print('CAMBIOS GUARDADOS')
            super().save_model(request, obj, form, change)
        else:
            self.message_user(
                request,
                'You are not allowed to perform this action',
                messages.ERROR)

    def delete_model(self, request, obj):
        qs = super().get_queryset(request)
        user_instance_permissions = get_objects_for_user(
            request.user, 'learning.delete_company', qs,
            accept_global_perms=False)
        print('test get user objects', user_instance_permissions)
        if user_instance_permissions:
            print('BORRADO REALIZADO')
            super().delete_model(request, obj)
        else:
            self.message_user(
                request,
                'You are not allowed to perform this action',
                messages.ERROR)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'learning.view_company', qs,
            accept_global_perms=False)


# Register your models here.
admin.site.register(Bot, BotAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile)
