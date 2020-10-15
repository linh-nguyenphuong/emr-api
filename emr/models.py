# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from user.models import User

class Emr(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, related_name='emr_patient', on_delete=models.Case)
    physician = models.ForeignKey(User, related_name='emr_physician', on_delete=models.Case)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='emr_created_by', on_delete=models.Case)
    status = models.CharField(max_length=20, default='initialized')
    total = models.DecimalField(max_digits=20, decimal_places=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'emr'

class EmrImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emr = models.ForeignKey(Emr, related_name='emr_image', on_delete=models.Case, null=True)
    url = models.CharField(max_length=191)

    class Meta:
        db_table = 'emr_image'