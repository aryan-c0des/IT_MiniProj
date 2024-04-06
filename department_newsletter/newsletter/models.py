from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def default_department():
    from .models import Department
    department, _ = Department.objects.get_or_create(name="General")
    return department.id


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=default_department)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Other profile fields if needed, such as profile picture, etc.
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


