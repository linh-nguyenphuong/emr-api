# Django imports
from django.conf.urls import url, include

# Application imports
from drug_unit.admin.views import (
    DrugUnitView,
    DrugUnitDetailsView,
)

urlpatterns = [
    url(r'^$', DrugUnitView.as_view(), name='list-create-drug_category'),
    url(r'^(?P<drug_unit_id>[0-9A-Fa-f-]+)/$', DrugUnitDetailsView.as_view(), name='detail-drug_category'),
]
