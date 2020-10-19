# Django imports
from django.conf.urls import url, include

# Application imports
from drug.admin.views import (
    DrugView,
    DrugDetailsView,
)

urlpatterns = [
    url(r'^$', DrugView.as_view(), name='list-create-drug'),
    url(r'^(?P<drug_id>[0-9A-Fa-f-]+)/$', DrugDetailsView.as_view(), name='detail-drug'),
]
