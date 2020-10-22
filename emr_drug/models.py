# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from emr.models import Emr
from drug_instruction.models import DrugInstruction
from drug.models import Drug

class EmrDrug(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emr = models.ForeignKey(Emr, related_name='emr_drug_emr', on_delete=models.Case)
    drug_instruction = models.ForeignKey(DrugInstruction, related_name='emr_drug_drug_instruction', on_delete=models.Case)
    drug = models.ForeignKey(Drug, related_name='emr_drug_drug', on_delete=models.Case)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'emr_drug'