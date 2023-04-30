from django.db import models
from users.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date

# null, blank

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # 할 일 저장 시간
    created_at = models.DateTimeField(auto_now_add=True)
    # title 수정 시간
    updated_at = models.DateTimeField(null=True, default=timezone.now)
    # 언제 할 일인지 저장!
    do_at = models.DateField(null=True, default=date.today)
    is_complete = models.BooleanField(default=False)
    # is_complete 변경 시간
    completion_at = models.DateTimeField(null=True, default=timezone.now)

    def get_absolute_url(self):
        return reverse('todo_detail_view', kwargs={'todo_id': self.id})

    def __str__(self):
        return self.title