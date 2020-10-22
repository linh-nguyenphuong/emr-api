# Django imports
from django.conf.urls import url

# Application imports
from setting.admin.views import (
    SettingView,
    SettingDetailsView
)

urlpatterns = [
    url(r'^$', SettingView.as_view(), name='setting-view'),
    url(r'^(?P<setting_id>[0-9A-Fa-f-]+)/$', SettingDetailsView.as_view(), name='setting-details'),
]
