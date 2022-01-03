from django.db import models
from home.models import Task
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Trash(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name=_("Trash task"), on_delete=models.CASCADE, related_name='trash_tasks')

    created_at = models.DateTimeField(_("Creation Date") ,auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated Date"), auto_now=True)

    def __str__(self) -> str:
        return self.task.title
    