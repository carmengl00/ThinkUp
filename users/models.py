from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password = None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username = username, email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        return self._create_user(username, email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank = False, max_length=254, verbose_name='email address', unique=True)
    username = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(default = timezone.now, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username