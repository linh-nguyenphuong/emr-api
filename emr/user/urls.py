# Django imports
from django.conf.urls import url, include

# Application imports
from emr.user.views import (
    EmrView,
    EmrDetailsView,

    EmrImageAddView,
    EmrImageRemoveView,

    EmrCompleteView,
    EmrPaidView,

    EmrPatientView,
    EmrPatientDetailsView
)

urlpatterns = [
    url(r'^$', EmrView.as_view(), name='user-list-create-emr'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrDetailsView.as_view(), name='user-detail-emr'),

    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/image/$', EmrImageAddView.as_view(), name='user-add-emr-image'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/image/(?P<emr_image_id>[0-9A-Fa-f-]+)/$', EmrImageRemoveView.as_view(), name='user-remove-emr-image'),

    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/complete/$', EmrCompleteView.as_view(), name='user-emr-complete'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/paid/$', EmrPaidView.as_view(), name='user-emr-paid'),

    url(r'^myemr/$', EmrPatientView.as_view(), name='patient-list-emr'),
    url(r'^myemr/(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrPatientDetailsView.as_view(), name='patient-details-emr'),
]
