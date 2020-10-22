# Django imports
from django.conf.urls import url, include

# Application imports
from service.user.views import (
    ServiceView,
    ServiceDetailsView,
)

urlpatterns = [
    url(r'^$', ServiceView.as_view(), name='user-list-service'),
    url(r'^(?P<service_id>[0-9A-Fa-f-]+)/$', ServiceDetailsView.as_view(), name='user-detail-service'),
]
