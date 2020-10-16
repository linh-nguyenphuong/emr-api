# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from user.models import User
from room.models import Room

class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, related_name='visit_room', on_delete=models.Case)
    patient = models.ForeignKey(User, related_name='visit_patient', on_delete=models.Case)
    visit_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='visit_created_by', on_delete=models.Case)
    status = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'visit'