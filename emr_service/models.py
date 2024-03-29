# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from service.models import Service
from emr.models import Emr

class EmrService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, related_name='emr_service_service', on_delete=models.Case)
    emr = models.ForeignKey(Emr, related_name='emr_service_emr', on_delete=models.Case)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'emr_service'