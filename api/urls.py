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
    url(r'^api/admin/manage-user/', include('user.admin.urls'), name='api-admin-user'),

    #------------------------------------------------------
    #                     User API                       
    #------------------------------------------------------
    # User
    url(r'^api/user/role/', include('role.user.urls'), name='api-user-role'),

    # Profile
    # url(r'^api/user/profile/', include('user.profile.urls'), name='api-user-profile'),
]
