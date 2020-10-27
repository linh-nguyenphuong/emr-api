# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from disease_category.models import DiseaseCategory

class Disease(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=191)
    code = models.CharField(max_length=191)
    disease_category = models.ForeignKey(DiseaseCategory, related_name='disease_category', on_delete=models.Case)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'disease'
