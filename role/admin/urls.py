# Django imports
from django.conf.urls import url

# Application imports
from .views import (
    ListCreateRoleView,
    DetailUpdateDestroyRoleView
)

urlpatterns = [
    url(r'^$', ListCreateRoleView.as_view(), name='list-create-role'),
    url(r'^(?P<flower_category_id>[0-9]+)/$', DetailUpdateDestroyRoleView.as_view(), name='detail-update-destroy-role'),
]
