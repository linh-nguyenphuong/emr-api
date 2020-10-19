# Django imports
from django.conf.urls import url, include

# Application imports
from disease_category.admin.views import (
    DiseaseCategoryView,
    DiseaseCategoryDetailsView,
)

urlpatterns = [
    url(r'^$', DiseaseCategoryView.as_view(), name='list-create-disease_category'),
    url(r'^(?P<disease_category_id>[0-9A-Fa-f-]+)/$', DiseaseCategoryDetailsView.as_view(), name='detail-disease_category'),
]
