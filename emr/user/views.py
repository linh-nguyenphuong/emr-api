# Python imports
import cloudinary
from pyfcm import FCMNotification

# Django imports
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings

# Django REST framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import (
    APIView,
)
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import (
    DjangoFilterBackend,
)

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
    IsAdminOrPhysician,
    IsPatient
)

# Model imports
from emr.models import (
    Emr,
    EmrImage
)
from emr_drug.models import EmrDrug
from emr_disease.models import EmrDisease
from emr_service.models import EmrService
from drug.models import Drug
from drug_instruction.models import DrugInstruction
from disease.models import Disease
from service.models import Service
from user.models import User

# Serialier imports
from emr.user.serializers import (
    EmrSerializer,
    EmrImageSerializer
)

class EmrView(generics.ListCreateAPIView):
    model = Emr
    serializer_class = EmrSerializer
    permission_classes = (IsAdminOrPhysician,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'patient__first_name',
        'patient__last_name'
    )
    filter_fields = (
        'created_at',
        'status', 
        'is_paid',
        'patient_id',
        'physician_id'
    )

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        total = 0
        patient = User.objects.filter(
            id=data.get('patient_id'),
            role__name='patient', 
            is_deleted=False
        )
        if not patient:
            raise ValidationError(ErrorTemplate.PATIENT_NOT_EXIST)
        
        physician = User.objects.filter(
            id=data.get('physician_id'),
            role__name='physician', 
            is_deleted=False
        )
        if not physician:
            raise ValidationError(ErrorTemplate.PHYSICIAN_NOT_EXIST)

        data['status'] = 'pending'
        serializer.save(created_by=self.request.user,
                        total=total)
        return Response(serializer.data)

class EmrDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Emr
    serializer_class = EmrSerializer
    permission_classes = (IsAdminOrPhysician,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        # Get serializer
        serializer = self.serializer_class(instance=emr)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        serializer = EmrSerializer(emr, data=request.data)
        serializer.is_valid(raise_exception=False)
        emr = serializer.save()

        return Response(self.serializer_class(emr).data)

    def delete(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        emr.__dict__.update(
            is_deleted=True,
        )

        EmrImage.objects.filter(emr=emr).update(is_deleted=True)
        EmrDrug.objects.filter(emr=emr).update(is_deleted=True)
        EmrDisease.objects.filter(emr=emr).update(is_deleted=True)
        EmrService.objects.filter(emr=emr).update(is_deleted=True)

        # Save to database
        emr.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        return obj

class EmrImageAddView(generics.CreateAPIView):
    model = EmrImage
    serializer_class = EmrImageSerializer
    permission_classes = (IsAdminOrPhysician,)
    lookup_url_kwarg = 'emr_id'

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(
            id=self.kwargs.get(self.lookup_url_kwarg),
            is_deleted=False
        ).first()
        if not emr:
            return Response(ErrorTemplate.EMR_NOT_EXIST, status.HTTP_400_BAD_REQUEST)
        
        # try:
        file = request.FILES.get('image')
        if not file:
            return Response(ErrorTemplate.IMAGE_REQUIRED, status.HTTP_400_BAD_REQUEST)

        uploaded_file = cloudinary.uploader.upload(
            file,
            folder='emr/emr_image/', 
        )

        emr_image = EmrImage(
            url=uploaded_file.get('secure_url'),
            emr=emr
        )

        # Save to database
        emr_image.save()

        serializer = self.serializer_class(instance=emr_image)
        # except:
        #     return Response(ErrorTemplate.UserError.CANNOT_UPLOAD_IMAGE, status.HTTP_417_EXPECTATION_FAILED)

        return Response(serializer.data)

class EmrImageRemoveView(generics.DestroyAPIView):
    model = EmrImage
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None
    lookup_url_kwarg = 'emr_image_id'

    def delete(self, request, *args, **kwargs):
        emr_image = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr_image:
            return Response(ErrorTemplate.IMAGE_NOT_EXIST, status.HTTP_400_BAD_REQUEST)

        emr_image.__dict__.update(
            is_deleted=True,
        )
        emr_image.save()

        return Response({
            'message': 'Deleted successfully'
        })

class EmrCompleteView(generics.RetrieveAPIView):
    model = EmrImage
    serializer_class = EmrSerializer
    permission_classes = (IsAdminOrPhysician,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        emr.status = 'completed'
        emr.save()

        return Response(self.serializer_class(emr).data)

class EmrPaidView(generics.RetrieveAPIView):
    model = EmrImage
    serializer_class = EmrSerializer
    permission_classes = (IsAdminOrPhysician,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        emr.is_paid = True
        emr.save()

        return Response(self.serializer_class(emr).data)

class EmrPatientView(generics.ListAPIView):
    model = Emr
    serializer_class = EmrSerializer
    permission_classes = (IsPatient,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    filter_fields = (
        'created_at',
        'status', 
        'is_paid',
        'physician_id'
    )

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False,
                                        patient_id=self.request.user.id).order_by('-created_at')

class EmrPatientDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Emr
    serializer_class = EmrSerializer
    permission_classes = (IsPatient,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        if not emr.patient == self.request.user:
            raise ValidationError(ErrorTemplate.CANNOT_ACCESS_EMR)

        # Get serializer
        serializer = self.serializer_class(instance=emr)

        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        return obj