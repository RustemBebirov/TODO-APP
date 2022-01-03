from django.contrib import admin
from .models import Task, Friends, TaskComment
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(Friends)