# Django imports
from django.conf.urls import url, include

# Application imports
from emr_disease.admin.views import (
    EmrDiseaseAddView,
    EmrDiseaseRemoveView,
)

urlpatterns = [
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrDiseaseAddView.as_view(), name='add-emr-disease'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/remove/(?P<emr_disease_id>[0-9A-Fa-f-]+)/$', EmrDiseaseRemoveView.as_view(), name='remove-enr-disease'),
]
