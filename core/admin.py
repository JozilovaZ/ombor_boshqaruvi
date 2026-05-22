from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Permission, UserSession, ActivityLog


class PermissionInline(admin.TabularInline):
    model = Permission
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('role',)}),
    )
    inlines = [PermissionInline]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu', 'permission_type', 'created_at')
    list_filter = ('menu', 'permission_type')
    search_fields = ('user__username',)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'created_at', 'last_activity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'ip_address')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('user',)
    search_fields = ('user__username', 'action')
