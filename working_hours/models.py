# Python imports
import uuid

# Django imports
from django.db import models

class WorkingHours(models.Model):
    weekday = models.CharField(max_length=20)
    is_closed = models.BooleanField(default=False)

    class Meta:
        db_table = 'working_hours'