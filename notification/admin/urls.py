# Django imports
from django.conf.urls import url

# Application imports
from notification.admin.views import (
    NotificationView,
    # RoleDetailsView
)

urlpatterns = [
    url(r'^$', NotificationView.as_view(), name='notification-view'),
]
