# Python imports
import uuid
import jwt
from datetime import datetime, timedelta
import os

# Django imports
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import (
    make_password,
    check_password
)

# Model imports
from role.models import Role

class AbstractUser(models.Model):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    
    is_anonymous = False
    is_authenticated = True

    objects = UserManager()

    class Meta:
        abstract = True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=191, null=True, blank=True, unique=True) 
    phone = models.CharField(max_length=30, null=True, blank=True, unique=True) # Patient use phone number to login
    first_name = models.CharField(max_length=191, null=True, blank=True)
    last_name = models.CharField(max_length=191, null=True, blank=True)
    address = models.CharField(max_length=191, null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    is_verified_phone = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=191)
    last_reset_password_at = models.DateTimeField(null=True)
    DOB = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.CharField(max_length=191, null=True, blank=True)
    fcm_registration = models.CharField(max_length=191, null=True, blank=True)
    role = models.ForeignKey(Role, related_name='user_role', on_delete=models.Case)
    is_deleted = models.BooleanField(default=False)
    job = models.CharField(max_length=191, null=True, blank=True)
    ethnicity = models.CharField(max_length=191, null=True, blank=True)
    expatriate = models.CharField(max_length=191, null=True, blank=True)
    workplace = models.CharField(max_length=191, null=True, blank=True)
    family_member_name = models.CharField(max_length=191, null=True, blank=True)
    family_member_address = models.CharField(max_length=191, null=True, blank=True)
    
    GENDER_CHOICES = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
        ('Khác', 'Khác')
    )
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='Nam')

    class Meta:
        db_table = 'user'

    @property
    def access_token(self):
        return self._generate_access_token()

    @property
    def refresh_token(self):
        return self._generate_refresh_token()

    @property
    def verify_email_token(self):
        return self._generate_verify_email_token()

    @property
    def verify_reset_password_token(self):
        return self._generate_verify_reset_password_token()

    def _generate_access_token(self):
        dt = datetime.now() + timedelta(hours=3)

        token = jwt.encode({
            'token_type': 'access',
            'user_id': str(self.id),
            'role': self.role.name,
            'expired_at': dt.strftime('%c')
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf8')

    def _generate_refresh_token(self):
        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode({
            'token_type': 'refresh',
            'user_id': str(self.id),
            'role': self.role.name,
            'expired_at': dt.strftime('%c'),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf8')


    def _generate_verify_email_token(self):
        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode({
            'token_type': 'verify_email',
            'user_id': str(self.id),
            'expired_at': dt.strftime('%c'),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf8')

    def _generate_verify_reset_password_token(self):
        token = jwt.encode({
            'token_type': 'verify_reset_password',
            'user_id': str(self.id),
            'created_at': str(datetime.now()),
            'expired_at': str(datetime.now() + timedelta(hours=3)),
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf8')