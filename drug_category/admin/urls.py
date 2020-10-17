# Django imports
from django.conf.urls import url, include

# Application imports
from drug_category.admin.views import (
    DrugCategoryView,
    DrugCategoryDetailsView,
)

urlpatterns = [
    url(r'^$', DrugCategoryView.as_view(), name='list-create-drug_category'),
    url(r'^(?P<drug_category_id>[0-9A-Fa-f-]+)/$', DrugCategoryDetailsView.as_view(), name='detail-drug_category'),
]
