# Python imports
import uuid

# Django imports
from django.db import models

class DrugCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=191)

    class Meta:
        db_table = 'drug_category'