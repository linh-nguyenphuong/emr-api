# Django imports
from django.conf.urls import url, include

# Application imports
from visit.admin.views import (
    VisitView,
    VisitDetailsView,
    PrintView
)

urlpatterns = [
    url(r'^$', VisitView.as_view(), name='list-create-visit'),
    url(r'^(?P<visit_id>[0-9A-Fa-f-]+)/$', VisitDetailsView.as_view(), name='detail-visit'),
    url(r'^print/$', PrintView.as_view(), name='print-visit'),

]
