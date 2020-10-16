from django.conf.urls import url

from .views import (
    CreateNotificationView,
    ListOwnerNotificationView,
)

urlpatterns = [
    url(r'^$', CreateNotificationView.as_view(), name='broadcast-notification'),
    url(r'^list/$', ListOwnerNotificationView.as_view(), name='list-notification'),
]