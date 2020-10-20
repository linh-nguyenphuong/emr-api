# Django imports
from django.conf.urls import url, include

# Application imports
from drug_instruction.user.views import (
    DrugInstructionView,
    DrugInstructionDetailsView,
)

urlpatterns = [
    url(r'^$', DrugInstructionView.as_view(), name='user-list-drug-instruction'),
    url(r'^(?P<drug_instruction_id>[0-9A-Fa-f-]+)/$', DrugInstructionDetailsView.as_view(), name='user-detail-drug-instruction'),
]
