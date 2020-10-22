# Django imports
from django.conf.urls import url, include

# Application imports
from patient_service.admin.views import (
    EmrServiceView,
    EmrServiceRemoveView,
)
#
urlpatterns = [
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrServiceView.as_view(), name='add-emr-service'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/remove/(?P<emr_service_id>[0-9A-Fa-f-]+)/$', EmrServiceRemoveView.as_view(), name='remove-enr-service'),
]
