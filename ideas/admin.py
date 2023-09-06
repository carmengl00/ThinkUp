from django.contrib import admin

from ideas.models import Idea, Notification

# Register your models here.
admin.site.register(Idea)
admin.site.register(Notification)