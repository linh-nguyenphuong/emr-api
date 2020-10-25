# Django imports
from django.conf.urls import url, include

# Application imports
from user.patient.views import (
    PatientView,
    PatientDetailsView,
)

urlpatterns = [
    url(r'^$', PatientView.as_view(), name='list-create-patient'),
    url(r'^(?P<patient_id>[0-9A-Fa-f-]+)/$', PatientDetailsView.as_view(), name='detail-patient'),
]
