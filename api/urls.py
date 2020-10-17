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
    url(r'^api/admin/manage-notification/', include('notification.admin.urls'), name='api-admin-notification'),
    url(r'^api/admin/manage-user/', include('user.admin.urls'), name='api-admin-user'),
    url(r'^api/admin/manage-drug-category/', include('drug_category.admin.urls'), name='api-admin-drug'),

    #------------------------------------------------------
    #                     User API
    #------------------------------------------------------
    # Profile
    url(r'^api/user/role/', include('role.user.urls'), name='api-user-role'),
]
