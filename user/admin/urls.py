from django.conf.urls import url

from .views import (
    ListCreateUserView,
    RetrieveUpdateDestroyUserView,
)

urlpatterns = [
    url(r'^$', ListCreateUserView.as_view(), name='list-create-user'),
    url(r'^list/$', RetrieveUpdateDestroyUserView.as_view(), name='retrieve-update-destroy-user'),
]