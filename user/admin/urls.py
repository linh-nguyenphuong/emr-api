# Django imports
from django.conf.urls import url, include

# Application imports
from user.admin.views import (
    UserView,
    UserDetailsView,
    BlockUser,
    UnblockUser,

    Dashboard
)

urlpatterns = [
    url(r'^$', UserView.as_view(), name='list-create-user'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/$', UserDetailsView.as_view(), name='detail-user'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/block/$', BlockUser.as_view(), name='block-user'),
    url(r'^(?P<user_id>[0-9A-Fa-f-]+)/unblock/$', UnblockUser.as_view(), name='unblock-user'),

    url(r'^dashboard/$', Dashboard.as_view(), name='unblock-user'),
]
