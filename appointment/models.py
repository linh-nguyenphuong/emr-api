# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from user.models import User

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    physician = models.ForeignKey(User, related_name='appointment_physician', on_delete=models.Case)
    patient = models.ForeignKey(User, related_name='appointment_patient', on_delete=models.Case)
    appointment_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='appointment_created_by', on_delete=models.Case)
    status = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'appointment'