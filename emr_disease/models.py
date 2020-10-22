# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from emr.models import Emr
from disease.models import Disease

class EmrDisease(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emr = models.ForeignKey(Emr, related_name='emr_disease_emr', on_delete=models.Case)
    disease = models.ForeignKey(Disease, related_name='emr_disease_disease', on_delete=models.Case)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'emr_disease'