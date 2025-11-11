# blogapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # optional: link task to blog or user if needed:
    # blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return self.title
