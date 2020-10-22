# Django imports
from django.conf.urls import url

# Application imports
from role.user.views import (
    RoleView,
    RoleDetailsView
)

urlpatterns = [
    url(r'^$', RoleView.as_view(), name='role-view'),
    url(r'^(?P<role_id>[0-9]+)/$', RoleDetailsView.as_view(), name='role-details'),
]
