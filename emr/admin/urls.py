# Django imports
from django.conf.urls import url, include

# Application imports
from emr.admin.views import (
    EmrView,
    EmrDetailsView,

    EmrImageAddView,
    EmrImageRemoveView,

    EmrCompleteView,
    EmrPaidView
)

urlpatterns = [
    url(r'^$', EmrView.as_view(), name='list-create-emr'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/$', EmrDetailsView.as_view(), name='detail-emr'),

    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/image/$', EmrImageAddView.as_view(), name='add-emr-image'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/image/(?P<emr_image_id>[0-9A-Fa-f-]+)/$', EmrImageRemoveView.as_view(),
        name='remove-enr-image'),

    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/complete/$', EmrCompleteView.as_view(), name='emr-complete'),
    url(r'^(?P<emr_id>[0-9A-Fa-f-]+)/paid/$', EmrPaidView.as_view(), name='emr-paid'),
]
