# Django imports
from django.conf.urls import url, include

# Application imports
from disease_category.user.views import (
    DiseaseCategoryView,
    DiseaseCategoryDetailsView,
)

urlpatterns = [
    url(r'^$', DiseaseCategoryView.as_view(), name='user-list-disease-category'),
    url(r'^(?P<disease_category_id>[0-9A-Fa-f-]+)/$', DiseaseCategoryDetailsView.as_view(), name='user-detail-disease-category'),
]
