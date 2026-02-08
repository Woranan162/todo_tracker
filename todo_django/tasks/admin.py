from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for Task model.
    """
    
    # Fields to display in the task list
    list_display = [
        'title',
        'user',
        'status',
        'priority',
        'due_date',
        'is_overdue',
        'created_at',
    ]
    
    # Filters in the sidebar
    list_filter = [
        'status',
        'priority',
        'created_at',
        'due_date',
        'user',
    ]
    
    # Search functionality
    search_fields = [
        'title',
        'description',
        'user__username',
        'user__email',
    ]
    
    # Fields that are clickable links
    list_display_links = ['title']
    
    # Fields that can be edited directly in the list view
    list_editable = ['status', 'priority']
    
    # Number of items per page
    list_per_page = 25
    
    # Ordering
    ordering = ['-created_at']
    
    # Date hierarchy navigation
    date_hierarchy = 'created_at'
    
    # Read-only fields
    readonly_fields = [
        'created_at',
        'updated_at',
        'completed_at',
        'is_overdue',
        'is_completed',
    ]
    
    # Fieldsets for the detail/edit page
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'description',
                'user',
            )
        }),
        ('Status & Priority', {
            'fields': (
                'status',
                'priority',
            )
        }),
        ('Dates', {
            'fields': (
                'due_date',
                'created_at',
                'updated_at',
                'completed_at',
            )
        }),
        ('Computed Fields', {
            'fields': (
                'is_overdue',
                'is_completed',
            ),
            'classes': ('collapse',),  # Collapsed by default
        }),
    )
    
    # Actions dropdown
    actions = ['mark_as_completed', 'mark_as_pending', 'mark_as_high_priority']
    
    def mark_as_completed(self, request, queryset):
        """
        Custom admin action to mark tasks as completed.
        """
        updated = 0
        for task in queryset:
            task.mark_complete()
            updated += 1
        self.message_user(request, f'{updated} task(s) marked as completed.')
    mark_as_completed.short_description = 'Mark selected tasks as completed'
    
    def mark_as_pending(self, request, queryset):
        """
        Custom admin action to mark tasks as pending.
        """
        updated = 0
        for task in queryset:
            task.mark_incomplete()
            updated += 1
        self.message_user(request, f'{updated} task(s) marked as pending.')
    mark_as_pending.short_description = 'Mark selected tasks as pending'
    
    def mark_as_high_priority(self, request, queryset):
        """
        Custom admin action to mark tasks as high priority.
        """
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} task(s) marked as high priority.')
    mark_as_high_priority.short_description = 'Mark selected tasks as high priority'