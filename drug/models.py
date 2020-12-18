# Python imports
import uuid

# Django imports
from django.db import models

# Model imports
from drug_category.models import DrugCategory
from drug_unit.models import DrugUnit
from drug_dosage_form.models import DrugDosageForm
from drug_route.models import DrugRoute

class Drug(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=191)
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    drug_category = models.ForeignKey(DrugCategory, related_name='drug_drug_category', on_delete=models.Case)
    drug_unit = models.ForeignKey(DrugUnit, related_name='drug_drug_unit', on_delete=models.Case)
    drug_dosage_form = models.ForeignKey(DrugDosageForm, related_name='drug_drug_dosage_form', on_delete=models.Case)
    drug_route = models.ForeignKey(DrugRoute, related_name='drug_drug_route', on_delete=models.Case, null=True)
    strength = models.CharField(max_length=191, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'drug'