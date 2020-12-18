# Django imports
from django.conf.urls import url, include

# Application imports
from drug_route.user.views import (
    DrugRouteDetailsView,
    DrugRouteView,
)

urlpatterns = [
    url(r'^$', DrugRouteView.as_view(), name='list-drug-route'),
    url(r'^(?P<drug_route_id>[0-9A-Fa-f-]+)/$', DrugRouteDetailsView.as_view(), name='detail-drug-route-form-user'),
]
