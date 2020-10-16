# Python imports
import uuid

# Django imports
from django.db import models

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'service'