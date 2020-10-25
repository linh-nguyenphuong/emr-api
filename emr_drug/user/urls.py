# Django imports
from django.conf.urls import url, include

# Application imports
from emr_drug.user.views import (
    EmrDrugAddView,
    EmrDrugDetailsView,
)

urlpatterns = [
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrDrugAddView.as_view(), name='user-add-emr-drug'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/(?P<emr_drug_id>[0-9A-Fa-f-]+)/$', EmrDrugDetailsView.as_view(), name='user-details-emr-drug'),
]
