# Python imports
import uuid

# Django imports
from django.db import models

class Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.CharField(max_length=191)
    value = models.CharField(max_length=191)

    class Meta:
        db_table = 'setting'