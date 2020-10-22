# Django imports
from django.conf.urls import url, include

# Application imports
from emr_drug.admin.views import (
    EmrDrugAddView,
    EmrDrugRemoveView,
)

urlpatterns = [
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrDrugAddView.as_view(), name='add-emr-drug'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/remove/(?P<emr_drug_id>[0-9A-Fa-f-]+)/$', EmrDrugRemoveView.as_view(), name='remove-enr-drug'),
]
