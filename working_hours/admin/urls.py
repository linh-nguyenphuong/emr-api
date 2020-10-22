# Django imports
from django.conf.urls import url

# Application imports
from working_hours.admin.views import (
    WorkingView,
    WorkingDetailsView
)

urlpatterns = [
    url(r'^$', WorkingView.as_view(), name='working-view'),
    url(r'^(?P<working_id>[0-9]+)/$', WorkingDetailsView.as_view(), name='working-details'),
]
