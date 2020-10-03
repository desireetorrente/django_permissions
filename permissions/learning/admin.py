from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Bot, Company, UserProfile
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from django.contrib import messages


class UserProfileAdmin(GuardedModelAdmin):
    pass


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


class UsersInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    fields = ('user', 'work_position')
    verbose_name = 'user'
    verbose_name_plural = 'users'

class CompanyAdmin(GuardedModelAdmin):
    list_display = ('name', 'created_by')
    inlines = [
        UsersInline,
        #BotsInline
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return super().has_view_permission(request, obj=obj)
            
        if request.user.has_perm('view_company', obj):
            return super().has_view_permission(request, obj=obj)
        
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('delete_company', obj):
            return super().has_delete_permission(request, obj=obj)
        
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.has_perm('change_company', obj):
            return super().has_change_permission(request, obj=obj)

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'learning.view_company', qs,
            accept_global_perms=False)


# Register your models here.
admin.site.register(Bot, BotAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
