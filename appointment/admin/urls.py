# Django imports
from django.conf.urls import url, include

# Application imports
from appointment.admin.views import (
    AppointmentView,
    AppointmentDetailsView,
    AppointmentAcceptView,
    AppointmentRejectView
)

urlpatterns = [
    url(r'^$', AppointmentView.as_view(), name='list-create-appointment'),
    url(r'^(?P<appointment_id>[0-9A-Fa-f-]+)/$', AppointmentDetailsView.as_view(), name='detail-appointment'),
    url(r'^(?P<appointment_id>[0-9A-Fa-f-]+)/accept/$', AppointmentAcceptView.as_view(), name='accept-appointment'),
    url(r'^(?P<appointment_id>[0-9A-Fa-f-]+)/reject/$', AppointmentRejectView.as_view(), name='reject-appointment'),
]
