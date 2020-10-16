from django.conf.urls import url

from .views import CreateNotificationView

urlpatterns = [
    url(r'^', CreateNotificationView.as_view(), name='broadcast-notification'),
]