# Django imports
from django.conf.urls import url, include

# Application imports
from room.user.views import (
    RoomView,
    RoomDetailsView,
)

urlpatterns = [
    url(r'^$', RoomView.as_view(), name='user-list-room'),
    url(r'^(?P<room_id>[0-9A-Fa-f-]+)/$', RoomDetailsView.as_view(), name='user-detail-room'),
]
