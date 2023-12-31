from django.db import models

from users.models import CustomUser

# Create your models here.
class VisibilityType(models.TextChoices):
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

class Idea(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VisibilityType.choices, default=VisibilityType.PUBLIC)

    def __str__(self):
        return self.text
    
class Notification(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)