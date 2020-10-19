# Django imports
from django.conf.urls import url, include

# Application imports
from drug_instruction.admin.views import (
    DrugInstructionView,
    DrugInstructionDetailsView,
)

urlpatterns = [
    url(r'^$', DrugInstructionView.as_view(), name='list-create-drug_instruction'),
    url(r'^(?P<drug_instruction_id>[0-9A-Fa-f-]+)/$', DrugInstructionDetailsView.as_view(), name='detail-drug_instruction'),
]
