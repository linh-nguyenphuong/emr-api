# Django imports
from django.conf.urls import url, include

# Application imports
from drug.user.views import (
    DrugView,
    DrugDetailsView,
)

urlpatterns = [
    url(r'^$', DrugView.as_view(), name='user-list-drug'),
    url(r'^(?P<drug_id>[0-9A-Fa-f-]+)/$', DrugDetailsView.as_view(), name='user-detail-drug'),
]
