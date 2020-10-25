# Python imports
from datetime import datetime, timedelta
import jwt

# Django imports
from django.core.mail import send_mail
from django.conf import settings
from django.utils import dateparse
from django.db.models import Q, Sum, Count
from django.utils import timezone


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

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
    IsUser
)
from templates.email_template import (
    EmailTemplate
)

# Model imports
from user.models import User
from role.models import Role
from emr.models import Emr
from emr_service.models import EmrService
from emr_drug.models import EmrDrug

# Serialier imports
from user.admin.serializers import (
    UserSerializer,

    FilterDateRangeFormatSerializer,
    ReportPatientSerializer
)
from emr.admin.serializers import EmrSerializer

class UserView(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    search_fields = (
        'first_name',
        'last_name',
        'email', 
        'phone'
    )
    filter_fields = {
        'role__name': ['exact'],
    }

    def get_queryset(self):
        return self.model.objects.filter(
            is_deleted=False
        ).order_by('created_at')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        # Check phone existed
        if not data.get('phone') or data.get('phone') == '':
            return Response(ErrorTemplate.PHONE_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone = self.model.objects.filter(
                phone=data.get('phone'),
            ).first()
            if phone:
                return Response(ErrorTemplate.PHONE_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)

        # Check role exist
        role = Role.objects.filter(
            id=data.get('role_id'),
        ).first()
        if not role:
            return Response(ErrorTemplate.ROLE_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            phone= data.get('phone'),
            DOB=data.get('DOB'),
            gender=data.get('gender'),
            role=role
        )
        user.set_password(data.get('password'))

        # Complete create account for Admin, Physcian, Receptionist
        if role.name in ('admin', 'receptionist', 'physician'):
            if not data.get('email') or data.get('email') == '':
                return Response(ErrorTemplate.EMAIL_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Check email existed
                email = self.model.objects.filter(
                    email=data.get('email'),
                ).first()
                if email:
                    return Response(ErrorTemplate.EMAIL_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)
                user.email = data.get('email')

        # Save to database
        user.save()

        # Send activation link to user's email address
        url = 'http://127.0.0.1:8000/api/auth/verify-email'
        token = user.verify_email_token
        send_mail(
            subject=EmailTemplate.EmailConfirmation.SUBJECT,
            html_message=EmailTemplate.EmailConfirmation.BODY.format(user.first_name, '{0}/{1}/'.format(url, token)),
            message='',
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        serializer = self.serializer_class(instance=user)
        return Response(serializer.data)

# Retrieve - Update - Delete User
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_object(user_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=user)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_object(user_id)
        
        # Get serializer
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        # Check phone existed
        if not data.get('phone') or data.get('phone') == '':
            return Response(ErrorTemplate.PHONE_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone = self.model.objects.filter(
                phone=data.get('phone'),
                is_deleted=False
            ).exclude(
                id=user.id
            ).first()
            if phone:
                return Response(ErrorTemplate.PHONE_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)

        # Check role exist
        role = Role.objects.filter(
            id=data.get('role_id'),
        ).first()
        if not role:
            return Response(ErrorTemplate.ROLE_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)    

        user.__dict__.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            phone=data.get('phone'),
            DOB=data.get('DOB'),
            gender=data.get('gender'),
            role_id=role.id
        )

        # Complete update account for User
        if data.get('email') and not data.get('email') == '':
            # Check email existed
            email = self.model.objects.filter(
                email=data.get('email'),
                is_deleted=False
            ).exclude(
                id=user.id
            ).first()
            if email:
                return Response(ErrorTemplate.EMAIL_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.email = email
                user.is_active = False

                # Send activation link to user's email address
                url = 'http://127.0.0.1:8000/api/auth/verify-email'
                token = user.verify_email_token
                send_mail(
                    subject=EmailTemplate.EmailConfirmation.SUBJECT,
                    html_message=EmailTemplate.EmailConfirmation.BODY.format(user.first_name, '{0}/{1}/'.format(url, token)),
                    message='',
                    from_email=settings.FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False
                )
            
        # Save to database
        user.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_object(user_id)

        user.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        user.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.USER_NOT_EXIST)

        return obj

# Block User
class BlockUser(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        # Check created account time
        if user.created_at > request.user.created_at:
            Response(ErrorTemplate.NOT_BLOCK_OLDER_ADMIN, status.HTTP_400_BAD_REQUEST)

        if user.is_active == True:
            user.__dict__.update(
                is_active=False,
                modified_by=request.user.id
            )
            user.save()

        return Response(serializer.data)

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.PROFILE_NOT_FOUND)

        return user

# Unblock User
class UnblockUser(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        if user.is_active == False:
            user.__dict__.update(
                is_active=True,
                modified_by=request.user.id
            )
            user.save()

        return Response(serializer.data)

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.PROFILE_NOT_FOUND)

        return user


class Dashboard(generics.RetrieveAPIView):
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):
        revenue = 0
        patient = User.objects.filter(is_deleted=False,
                                      role__name='patient').count()
        list_emr = Emr.objects.filter(is_paid=True,
                                 is_deleted=False)
        for emr in list_emr:
            # service
            list_service = EmrService.objects.filter(emr=emr,
                                                         is_deleted=False)
            for service in list_service:
                revenue = revenue + service.service.price
            # drug
            list_drug = EmrDrug.objects.filter(emr=emr,
                                               is_deleted=False)
            for drug in list_drug:
                revenue = revenue + (drug.quantity * drug.unit_price)
        return Response(
            dict(patient=patient,
                 revenue=revenue)
        )


class Report(generics.RetrieveAPIView):
    permission_classes = (IsAdmin,)

    def get(self, request, *args, **kwargs):
        from_date = self.request.query_params.get('from_date', timezone.now().min)
        to_date = self.request.query_params.get('to_date', timezone.now())
        from_date, to_date = self.validate_range_dates(from_date, to_date)

        patient_month = self.patient_monthly(from_date, to_date)

        revenue = self.revenue_monthly(from_date, to_date)

        list_emr = Emr.objects.filter(is_paid=True,
                                      is_deleted=False).order_by('-created_at')[:10]
        report_emr = []
        report_emr.append(ReportPatientSerializer(list_emr, many=True).data)
        return Response(
            dict(patient=patient_month,
                 list_emr=report_emr,
                 revenue=revenue)
        )

    def revenue_monthly(self, from_date, to_date):
        queryset = []
        for year_month in self.find_months(from_date, to_date):

            list_emr = Emr.objects.filter(is_paid=True,
                                          is_deleted=False,
                                          created_at__year=year_month[0],
                                          created_at__month=year_month[1],
                                          )
            revenue = 0
            for emr in list_emr:
                # service
                list_service = EmrService.objects.filter(emr=emr,
                                                             is_deleted=False)
                for service in list_service:
                    revenue = revenue + service.service.price
                # drug
                list_drug = EmrDrug.objects.filter(emr=emr,
                                                   is_deleted=False)
                for drug in list_drug:
                    revenue = revenue + (drug.quantity * drug.unit_price)
            queryset.append(
                {
                    "month": year_month[1],
                    "year": year_month[0],
                    "total_revenue": revenue
                }
            )
        return queryset

    def patient_monthly(self, from_date, to_date):
        queryset = []
        for year_month in self.find_months(from_date, to_date):
            queryset.append(
                {
                    "month": year_month[1],
                    "year": year_month[0],
                    "total_user": User.objects.filter(
                        is_deleted=False,
                        role__name='patient',
                        created_at__year=year_month[0],
                        created_at__month=year_month[1],
                    ).count(),
                }
            )
        return queryset

    @staticmethod
    def find_months(from_date, to_date):
        # Convert str to date
        if type(from_date) == str:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        if type(to_date) == str:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        print((to_date + timedelta(days=1) - from_date).days)

        total_months = lambda dt: dt.month + 12 * dt.year
        list_months = []
        for tot_m in range(total_months(from_date) - 1, total_months(to_date)):
            y, m = divmod(tot_m, 12)
            year_month = datetime(y, m + 1, 1).strftime("%Y-%m").split('-')
            year_month = list(map(int, year_month))
            list_months.append(year_month)

        return list_months

    @staticmethod
    def validate_range_dates(from_date, to_date, filter_type='report'):
        if not from_date or not to_date:
            raise ValidationError(dict(message='from_date and to_date is required'
            ))
        from_date, to_date = FilterRangeDate.validate_filter_range_date(from_date, to_date, filter_type)
        return from_date, to_date


class FilterRangeDate:

    @staticmethod
    def validate_filter_range_date(from_date, to_date, lang='en'):
        range_date_data = dict()
        if type(from_date) == str:
            range_date_data['from_date'] = from_date
        if type(to_date) == str:
            range_date_data['to_date'] = to_date
        date_serializer = FilterDateRangeFormatSerializer(data=range_date_data)
        date_serializer.is_valid(raise_exception=True)

        if type(from_date) == str and type(to_date) == str and from_date > to_date:
            raise ValidationError(dict(message='rom_date cannot be later than to_date'))

        if type(from_date) == str:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date().strftime('%Y-%m-%d')

        if type(to_date) == str:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            to_date = (to_date + timedelta(days=1)).strftime('%Y-%m-%d')

        return from_date, to_date
