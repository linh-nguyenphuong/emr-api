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

    url(r'^api/admin/manage-role/', include('role.admin.urls'), name='api-admin-role'),

    url(r'^api/admin/manage-drug-category/', include('drug_category.admin.urls'), name='api-admin-drug-category'),
    url(r'^api/admin/manage-drug-unit/', include('drug_unit.admin.urls'), name='api-admin-drug-unit'),
    url(r'^api/admin/manage-drug/', include('drug.admin.urls'), name='api-admin-drug'),
    url(r'^api/admin/manage-drug-instruction/', include('drug_instruction.admin.urls'), name='api-admin-drug-instruction'),

    url(r'^api/admin/manage-disease-category/', include('disease_category.admin.urls'), name='api-admin-disease-category'),
    url(r'^api/admin/manage-disease/', include('disease.admin.urls'), name='api-admin-disease'),

    url(r'^api/admin/manage-service/', include('service.admin.urls'), name='api-admin-service'),

    url(r'^api/admin/manage-working-hours/', include('working_hours.admin.urls'), name='api-admin-service'),

    url(r'^api/admin/manage-setting/', include('setting.admin.urls'), name='api-admin-setting'),

    #------------------------------------------------------
    #                     User API
    #------------------------------------------------------
    # Role
    url(r'^api/user/role/', include('role.user.urls'), name='api-user-role'),

    # Profile
    url(r'^api/user/profile/', include('user.profile.urls'), name='api-user-profile'),
]
