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

    # Drug dosage form
    url(r'^api/admin/manage-drug-dosage-form/', include('drug_dosage_form.admin.urls'), name='api-admin-drug-dosage-form'),

    # Drug route
    url(r'^api/admin/manage-drug-route/', include('drug_route.admin.urls'), name='api-admin-drug-route'),

    # Disease category
    url(r'^api/admin/manage-disease-category/', include('disease_category.admin.urls'), name='api-admin-disease-category'),

    # Disease
    url(r'^api/admin/manage-disease/', include('disease.admin.urls'), name='api-admin-disease'),

    # Service
    url(r'^api/admin/manage-service/', include('service.admin.urls'), name='api-admin-service'),

    # Working hours
    url(r'^api/admin/manage-working-hours/', include('working_hours.admin.urls'), name='api-admin-working'),

    # Setting
    url(r'^api/admin/manage-setting/', include('setting.admin.urls'), name='api-admin-setting'),

    # Room
    url(r'^api/admin/manage-room/', include('room.admin.urls'), name='api-admin-room'),

    # Working hours
    url(r'^api/admin/manage-working-hours/', include('working_hours.admin.urls'), name='api-admin-service'),

    # Settings
    url(r'^api/admin/manage-setting/', include('setting.admin.urls'), name='api-admin-setting'),

    # Room
    url(r'^api/admin/manage-room/', include('room.admin.urls'), name='api-admin-room'),

    # Appointment
    url(r'^api/admin/manage-appointment/', include('appointment.admin.urls'), name='api-admin-appointment'),

    # Visit
    url(r'^api/admin/manage-visit/', include('visit.admin.urls'), name='api-admin-visit'),

    # Emr
    url(r'^api/admin/manage-emr/', include('emr.admin.urls'), name='api-admin-emr'),

    # Emr drug
    url(r'^api/admin/manage-emr-drug/', include('emr_drug.admin.urls'), name='api-admin-emr-drug'),

    # Emr disease
    url(r'^api/admin/manage-emr-disease/', include('emr_disease.admin.urls'), name='api-admin-emr-disease'),

    # Emr service
    url(r'^api/admin/manage-emr-service/', include('emr_service.admin.urls'), name='api-admin-emr-service'),

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

    # Drug dosage form
    url(r'^api/user/drug-dosage-form/', include('drug_dosage_form.user.urls'), name='api-user-drug-dosage-form'),

    # Drug route
    url(r'^api/user/drug-route/', include('drug_route.user.urls'), name='api-user-drug-route'),

    # Room
    url(r'^api/user/room/', include('room.user.urls'), name='api-user-room'),

    # Service
    url(r'^api/user/service/', include('service.user.urls'), name='api-user-service'),

    # Appointment
    url(r'^api/user/appointment/', include('appointment.user.urls'), name='api-user-appointment'),

    # Visit
    url(r'^api/user/visit/', include('visit.user.urls'), name='api-user-visit'),

    # Emr
    url(r'^api/user/emr/', include('emr.user.urls'), name='api-user-emr'),

    # Emr disease
    url(r'^api/user/emr-disease/', include('emr_disease.user.urls'), name='api-user-emr-disease'),

    # Emr service
    url(r'^api/user/emr-service/', include('emr_service.user.urls'), name='api-user-emr-service'),

    # Emr drug
    url(r'^api/user/emr-drug/', include('emr_drug.user.urls'), name='api-user-emr-drug'),

    # Patient
    url(r'^api/user/patient/', include('user.patient.urls'), name='api-user-patient'),
]
