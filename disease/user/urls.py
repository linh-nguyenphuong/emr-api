# Django imports
from django.conf.urls import url, include

# Application imports
from disease.user.views import (
    DiseaseView,
    DiseaseDetailsView,
)

urlpatterns = [
    url(r'^$', DiseaseView.as_view(), name='user-list-disease'),
    url(r'^(?P<disease_id>[0-9A-Fa-f-]+)/$', DiseaseDetailsView.as_view(), name='user-detail-disease'),
]
