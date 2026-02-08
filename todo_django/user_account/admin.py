from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin interface for User model.
    Extends Django's built-in UserAdmin.
    """
    
    # Fields to display in the user list
    list_display = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_active', 
        'is_staff',
        'date_joined'
    ]
    
    # Filters in the sidebar
    list_filter = [
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'date_joined'
    ]
    
    # Search functionality
    search_fields = [
        'username', 
        'email', 
        'first_name', 
        'last_name'
    ]
    
    # Fields that are clickable links
    list_display_links = ['username', 'email']
    
    # Number of items per page
    list_per_page = 25
    
    # Ordering
    ordering = ['-date_joined']
    
    # Fieldsets for the detail/edit page
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email',
                'first_name',
                'last_name',
                'password1', 
                'password2',
                'is_active',
                'is_staff'
            ),
        }),
    )