from django.contrib import admin
from .models import ContentBlock, Like, Comment, Rating  # ← ajoute Comment ici

@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('key', 'content')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'session_key', 'created_at')
    list_filter = ('content_type',)

@admin.register(Comment)  # ← maintenant Comment est importé
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'content_object', 'created_at')
    list_filter = ('content_type',)
    

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('value', 'content_object', 'session_key', 'created_at')
    list_filter = ('value', 'content_type')