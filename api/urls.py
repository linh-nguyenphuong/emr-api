from django.conf.urls import url, include
from .views import (
    index
)
urlpatterns = [
    url(r'^$', index),
    
    # Authentication
    url(r'^api/auth/', include('user.auth.urls'), name='api-auth'),

    #------------------------------------------------------
    #                     Admin API
    #------------------------------------------------------
    # Notification
    url(r'^api/admin/manage-notification/', include('notification.admin.urls'), name='api-admin-notification'),

    # User
    url(r'^api/admin/manage-user/', include('user.admin.urls'), name='api-admin-user'),
    # Role
    url(r'^api/admin/manage-role/', include('role.admin.urls'), name='api-admin-role'),
    # Drug category
    url(r'^api/admin/manage-drug-category/', include('drug_category.admin.urls'), name='api-admin-drug-category'),
    # Drug unit
    url(r'^api/admin/manage-drug-unit/', include('drug_unit.admin.urls'), name='api-admin-drug-unit'),
    # Drug
    url(r'^api/admin/manage-drug/', include('drug.admin.urls'), name='api-admin-drug'),
    # Drug instruction
    url(r'^api/admin/manage-drug-instruction/', include('drug_instruction.admin.urls'), name='api-admin-drug-instruction'),
    # Disease category
    url(r'^api/admin/manage-disease-category/', include('disease_category.admin.urls'), name='api-admin-disease-category'),
    # Disease
    url(r'^api/admin/manage-disease/', include('disease.admin.urls'), name='api-admin-disease'),
    # Service
    url(r'^api/admin/manage-service/', include('service.admin.urls'), name='api-admin-service'),
    # Working hours
    url(r'^api/admin/manage-working-hours/', include('working_hours.admin.urls'), name='api-admin-service'),
    # Settings
    url(r'^api/admin/manage-setting/', include('setting.admin.urls'), name='api-admin-setting'),
    # Room
    url(r'^api/admin/manage-room/', include('room.admin.urls'), name='api-admin-room'),
    # Appointment
    url(r'^api/admin/manage-appointment/', include('appointment.admin.urls'), name='api-admin-appointment'),

    url(r'^api/admin/manage-visit/', include('visit.admin.urls'), name='api-admin-visit'),

    url(r'^api/admin/manage-emr/', include('emr.admin.urls'), name='api-admin-emr'),

    #------------------------------------------------------
    #                     User API
    #------------------------------------------------------
    # Role
    url(r'^api/user/role/', include('role.user.urls'), name='api-user-role'),
    # Profile
    url(r'^api/user/profile/', include('user.profile.urls'), name='api-user-profile'),
    # Disease category
    url(r'^api/user/disease-category/', include('disease_category.user.urls'), name='api-user-disease-category'),
    # Disease
    url(r'^api/user/disease/', include('disease.user.urls'), name='api-user-disease'),
    # Drug category
    url(r'^api/user/drug-category/', include('drug_category.user.urls'), name='api-user-drug-category'),
    # Drug
    url(r'^api/user/drug/', include('drug.user.urls'), name='api-user-drug'),
    # Drug instruction
    url(r'^api/user/drug-instruction/', include('drug_instruction.user.urls'), name='api-user-drug-instruction'),
    # Drug unit
    url(r'^api/user/drug-unit/', include('drug_unit.user.urls'), name='api-user-drug-unit'),
    # Room
    url(r'^api/user/room/', include('room.user.urls'), name='api-user-room'),
    # Service
    url(r'^api/user/service/', include('service.user.urls'), name='api-user-service'),
    # Appointment
    url(r'^api/user/appointment/', include('appointment.user.urls'), name='api-user-appointment'),
]
