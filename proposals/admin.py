from django.contrib import admin
from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'client_name', 'budget', 'timeline', 'created_at']
    list_filter = ['created_at']
    search_fields = ['project_title', 'project_description', 'client_name']
    readonly_fields = ['created_at', 'updated_at', 'embedding']

    fieldsets = (
        ('Project Information', {
            'fields': ('project_title', 'project_description', 'requirements', 'client_name')
        }),
        ('Budget & Timeline', {
            'fields': ('budget', 'timeline')
        }),
        ('Generated Content', {
            'fields': ('generated_proposal',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )