from django.contrib import admin

from .models import Conversation, Comment, Notification, Vote


class CommentInline(admin.TabularInline):
    model = Comment


class VoteInline(admin.TabularInline):
    model = Vote


class ConversationAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'description', 'dialog', 'response', 'polis_id',
              'comment_nudge', 'comment_nudge_interval', 'comment_nudge_global_limit',
              'background_image', 'background_color', 'polis_url', 'polis_slug',
              'position', 'is_new']
    list_display = ['id', 'title', 'author', 'created_at', 'updated_at']


class CommentAdmin(admin.ModelAdmin):
    fields = ['conversation', 'author', 'content', 'polis_id', 'approval', 'rejection_reason']
    list_display = ['id', 'content', 'conversation', 'created_at', 'approval']
    list_editable = ['approval', ]
    list_filter = ['conversation', 'approval']
    inlines = [VoteInline]

class NotificationAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'url', 'seen', 'user', 'image']
    list_display = ['id', 'title', 'description', 'user', 'created_at']

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
