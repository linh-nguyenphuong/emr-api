# Django imports
from django.conf.urls import url, include

# Application imports
from user.profile.views import (
    ProfileDetailsView,
    UploadUserAvatarView
)

urlpatterns = [
    url(r'^$', ProfileDetailsView.as_view(), name='profile-view'),
    url(r'^avatar/$', UploadUserAvatarView.as_view(), name='upload-user-avatar-view'),
]
