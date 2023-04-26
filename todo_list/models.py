from django.db import models
from users.models import User
from django.urls import reverse
from django.utils import timezone

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=timezone.now)
    is_complete = models.BooleanField(default=False)
    completion_at = models.DateTimeField(null=True, default=timezone.now)

    def get_absolute_url(self):
        return reverse('todo_detail_view', kwargs={'todo_id': self.id})

    def __str__(self):
        return self.title