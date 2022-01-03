from django.contrib.auth.decorators import permission_required
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
User =get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50, unique=True)
    finish_date = models.DateTimeField(_("Finish time"),)
    detail = models.TextField(_("Detail"))
    reminder = models.BooleanField(_("Reminder"),default=False)
    done = models.BooleanField(_("Task Done"),default=False)
    privacy = models.BooleanField(_("Privacy"),default=False)

    created_at = models.DateTimeField(_("Creation Date") ,auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated Date"), auto_now=True)

    def get_absolute_url(self):
        return reverse('update_task', kwargs={"pk": self.pk})


    def __str__(self) -> str:
        return f'{self.title}-{self.user}'



class Friends(models.Model):
    friend = models.ForeignKey(User, verbose_name=_("Friends"), on_delete=models.CASCADE,related_name='shared_friends')
    task = models.ForeignKey(Task, verbose_name=_("Shared Task"), on_delete=models.CASCADE, related_name='shared_tasks')
    is_edit = models.BooleanField(_("Edit"),default=False)


    created_at = models.DateTimeField(_("Creation Date") ,auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated Date"), auto_now=True)

    def __str__(self) -> str:
        return f'{self.task.title}-{self.friend}e paylasib'

    

class TaskComment(models.Model):
    task = models.ForeignKey(Task, verbose_name=_("Task"), on_delete=models.CASCADE,related_name='task_comments')
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE,related_name='user_comments')
    detail = models.TextField(_("Comment Detail"))

    created_at = models.DateTimeField(_("Creation Date") ,auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated Date"), auto_now=True)

    def __str__(self) -> str:
        return self.detail

