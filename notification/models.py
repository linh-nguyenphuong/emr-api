# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from user.models import User

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=191)
    content = models.TextField()
    sender = models.ForeignKey(User, related_name='notification_sender', on_delete=models.Case)
    receiver = models.ForeignKey(User, related_name='notification_receiver', on_delete=models.Case)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'