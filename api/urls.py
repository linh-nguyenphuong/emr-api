from django.conf.urls import url, include
from .views import (
    index
)

urlpatterns = [
    url(r'^$', index),
    
    #Authentication
    url(r'^api/auth/', include('user.auth.urls'), name='api-auth'),

    #------------------------------------------------------
    #                     Admin API
    #------------------------------------------------------
    # User
    url(r'^api/admin/notification/', include('notification.admin.urls'), name='api-admin-notification')
    # url(r'^api/admin/manage-user/', include('user.admin.urls'), name='api-admin-user'),

    #------------------------------------------------------
    #                     User API                       
    #------------------------------------------------------
    # Profile
    # url(r'^api/user/profile/', include('user.profile.urls'), name='api-user-profile'),
]
