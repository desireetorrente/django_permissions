from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from guardian.admin import GuardedModelAdmin, GuardedModelAdminMixin
from guardian.shortcuts import get_objects_for_user

from .models import Bot, Company, UserProfile
from .forms import UserChangeForm, UserCreationForm



class BotsInline(admin.TabularInline):
    model = Bot


class UsersInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    fields = ('user', 'work_position')
    readonly_fields = ('user',)
    verbose_name = 'user'
    verbose_name_plural = 'users'

    def has_add_permission(self, request, obj):
        return False


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    fields = ('company', 'role',)
    verbose_name = 'profesional info'
    verbose_name_plural = 'profesional info'


class UserAdmin(GuardedModelAdminMixin, BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    
    inlines = [
        UserProfileInline
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )
    personalinfo_fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
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
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            return ( 
                self.fieldsets + 
                self.personalinfo_fieldsets + 
                self.permission_fieldsets + 
                self.importantdates_fieldsets
            )

        return ( 
                self.fieldsets + 
                self.personalinfo_fieldsets
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

    make_published.short_description = "Publish bot"


class CompanyAdmin(GuardedModelAdmin):
    list_display = ('name', 'created_by')
    inlines = [
        UsersInline
    ]

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
#admin.site.register(UserProfile, UserProfileAdmin)
