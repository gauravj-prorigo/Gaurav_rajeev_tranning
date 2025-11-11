# blogapp/serializers.py
from rest_framework import serializers
from .models import Blog, Task

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']
