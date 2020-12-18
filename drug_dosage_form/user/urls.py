# Django imports
from django.conf.urls import url, include

# Application imports
from drug_dosage_form.user.views import (
    DrugDosageFormDetailsView,
    DrugDosageFormView,
)

urlpatterns = [
    url(r'^$', DrugDosageFormView.as_view(), name='list-drug-dosage-form'),
    url(r'^(?P<drug_dosage_form_id>[0-9A-Fa-f-]+)/$', DrugDosageFormDetailsView.as_view(), name='detail-drug-dosage-form-user'),
]
