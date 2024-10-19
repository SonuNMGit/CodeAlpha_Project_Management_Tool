from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[
        ('manager', 'Manager'),
        ('team_member', 'Team Member')
    ])

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    team_members = models.ManyToManyField(User, related_name='team_projects')
    deadline = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,related_name='tasks', on_delete=models.CASCADE)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title

class TaskLink(models.Model):
    task = models.ForeignKey(Task, related_name='links', on_delete=models.CASCADE)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"