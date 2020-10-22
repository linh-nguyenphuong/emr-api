# Django imports
from django.conf.urls import url, include

# Application imports
from emr.admin.views import (
    EmrView,
    # EmrDetailsView,
)

urlpatterns = [
    url(r'^$', EmrView.as_view(), name='list-create-drug'),
    # url(r'^(?P<drug_id>[0-9A-Fa-f-]+)/$', EmrDetailsView.as_view(), name='detail-drug'),
]
