# Django imports
from django.conf.urls import url, include

# Application imports
from room.admin.views import (
    RoomView,
    RoomDetailsView,
)

urlpatterns = [
    url(r'^$', RoomView.as_view(), name='list-create-room'),
    url(r'^(?P<room_id>[0-9A-Fa-f-]+)/$', RoomDetailsView.as_view(), name='detail-room'),
]
