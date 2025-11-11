# blogapp/admin.py
from django.contrib import admin
from .models import Blog, Task

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completed', 'created_at')
    list_filter = ('completed',)
    search_fields = ('title',)
