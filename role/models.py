# Python imports
import uuid

# Django imports
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=191)

    class Meta:
        db_table = 'role'