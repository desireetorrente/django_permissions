from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from guardian.admin import GuardedModelAdmin, GuardedModelAdminMixin
from guardian.shortcuts import get_objects_for_user

from .models import Bot, Company
from .forms import UserChangeForm, UserCreationForm


class BotsInline(admin.TabularInline):
    model = Bot


class UserAdmin(GuardedModelAdminMixin, BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )
    professionalinfo_fieldsets = (
        (_('Professional info'), {'fields': (
            'first_name', 
            'last_name', 
            'email',
            'company', 
            'role', 
            'work_position'
        )}),
    )
    permission_fieldsets = (
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    importantdates_fieldsets = (
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'company', 'role'),
        }),
    )

    list_display = ('username', 'email', 'company', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'company')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            return (
                self.fieldsets +
                self.professionalinfo_fieldsets +
                self.permission_fieldsets +
                self.importantdates_fieldsets
            )

        return (
                self.fieldsets +
                self.professionalinfo_fieldsets
            )

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('view_user', obj):
            return super().has_view_permission(request, obj=obj)

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('delete_user', obj):
            return super().has_delete_permission(request, obj=obj)

        return False

    def has_change_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('change_user', obj):
            return super().has_change_permission(request, obj=obj)

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'view_user', qs,
            accept_global_perms=False)

    def save_model(self, request, user, form, change):
        super().save_model(request, user, form, change)

        if not (request.user.is_superuser or change):
            user.grant_permissions(request.user)
            user.grant_company_permissions()


class UserProfileAdmin(GuardedModelAdmin):

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('view_userprofile', obj):
            return super().has_view_permission(request, obj=obj)

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('delete_userprofile', obj):
            return super().has_delete_permission(request, obj=obj)

        return False

    def has_change_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('change_userprofile', obj):
            return super().has_change_permission(request, obj=obj)

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'view_userprofile', qs,
            accept_global_perms=False)


class BotAdmin(GuardedModelAdmin):
    list_display = ('name', 'company', 'created_by')
    actions = ['make_published']

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('view_bot', obj):
            return super().has_view_permission(request, obj=obj)

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('delete_bot', obj):
            return super().has_delete_permission(request, obj=obj)

        return False

    def has_change_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('change_bot', obj):
            return super().has_change_permission(request, obj=obj)

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'view_bot', qs,
            accept_global_perms=False)

    def make_published(self, request, queryset):
        if request.user.has_perm('bot_publish'):
            updated = get_objects_for_user(
                request.user, 'bot_publish',
                queryset)
            self.message_user(
                request,
                'Selected bots successfully published.',
                messages.SUCCESS)
        else:
            self.message_user(
                request,
                'You are not allowed to perform this action',
                messages.ERROR)

    def save_model(self, request, bot, form, change):
        super().save_model(request, bot, form, change)

        if not (request.user.is_superuser or change):
            bot.grant_permissions(request.user)

        User = get_user_model()
        profiles = bot.company.userprofile_set.all()
        # Profiles with Admin Permissions Template
        users_admin_template = User.objects.filter(
            userprofile__in=profiles,
            groups__name='Admin Permissions Template')
        if users_admin_template:
            bot.bulk_grant_permissions(
                'Admin Permissions Template',
                users_admin_template
            )

        # Profiles with Agent Permissions Template
        users_agent_template = User.objects.filter(
            userprofile__in=profiles,
            groups__name='Agent Permissions Template')

        if users_agent_template:
            bot.bulk_grant_permissions(
                'Agent Permissions Template',
                users_agent_template
            )

        # Profiles with Employee Permissions Template
        users_employee_template = User.objects.filter(
            userprofile__in=profiles,
            groups__name='Employee Permissions Template')

        if users_employee_template:
            bot.bulk_grant_permissions(
                'Employee Permissions Template',
                users_employee_template
            )

    make_published.short_description = "Publish bot"


class CompanyAdmin(GuardedModelAdmin):
    list_display = ('name', )

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('view_company', obj):
            return super().has_view_permission(request, obj=obj)

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('delete_company', obj):
            return super().has_delete_permission(request, obj=obj)

        return False

    def has_change_permission(self, request, obj=None):
        if obj is None or request.user.has_perm('change_company', obj):
            return super().has_change_permission(request, obj=obj)

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_objects_for_user(
            request.user, 'learning.view_company', qs,
            accept_global_perms=False)

    def save_model(self, request, company, form, change):
        super().save_model(request, company, form, change)

        if not (request.user.is_superuser or change):
            company.grant_permissions(request.user)


# Now register the new UserAdmin...
admin.site.register(get_user_model(), UserAdmin)
# Register the rest of your models here
admin.site.register(Bot, BotAdmin)
admin.site.register(Company, CompanyAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
