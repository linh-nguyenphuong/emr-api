# Django imports
from django.conf.urls import url, include

# Application imports
from drug_unit.user.views import (
    DrugUnitView,
    DrugUnitDetailsView,
)

urlpatterns = [
    url(r'^$', DrugUnitView.as_view(), name='user-list-drug-category'),
    url(r'^(?P<drug_unit_id>[0-9A-Fa-f-]+)/$', DrugUnitDetailsView.as_view(), name='user-detail-drug-category'),
]
