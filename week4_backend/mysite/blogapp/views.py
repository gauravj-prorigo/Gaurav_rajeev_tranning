# blogapp/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Blog, Task
from .serializers import BlogSerializer, TaskSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]  # change to IsAuthenticated when you enable auth

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]  # change later for auth
