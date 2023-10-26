from django.db import models
import uuid
from users.models import CustomUser

# Create your models here.
class VisibilityType(models.TextChoices):
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

class Idea(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=20, choices=VisibilityType.choices, default=VisibilityType.PUBLIC)

    def __str__(self):
        return self.text
    
class Notification(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)