"""
    Comment model admin definitions
    ===============================

    This module defines admin classes used to populate the Django administration dashboard.

"""

from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ The Comment model admin. """

    list_display = ('id', 'truncated_content', 'commented_object', 'created_at')
    list_display_links = ('id', 'truncated_content')
    list_filter = ('created_at', )
    raw_id_fields = ('registered_author', )
