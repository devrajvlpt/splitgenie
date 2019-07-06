# -*- coding: utf-8 -*-
# python manage.py make migrations your_app_label
# python manage.py migrate --fake-initial your_app_label

from __future__ import unicode_literals
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class ContactManager(BaseUserManager):

    """Summary
    """

    def create_user(self, mobile_number, password=None):
        """
        Creates and saves a User with the given mobile_number and password.
        
        Args:
            mobile_number (TYPE): Description
            password (None, optional): Description
        
        Returns:
            TYPE: Description
        
        Raises:
            ValueError: Description
        """
        if not mobile_number:
            raise ValueError('Users must have an mobile_number address')

        user = self.model(
            mobile_number=mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, mobile_number, password):
        """
        Creates and saves a staff user with the given mobile_number and password.
        
        Args:
            mobile_number (TYPE): Description
            password (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        user = self.create_user(
            mobile_number,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password):
        """
        Creates and saves a superuser with the given mobile_number and password.
        
        Args:
            mobile_number (TYPE): Description
            password (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        user = self.create_user(
            mobile_number,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class Contact(AbstractBaseUser, PermissionsMixin):

    """Summary
    
    Attributes:
        mobile_number (TYPE): Description
        objects (TYPE): Description
    """
    objects = ContactManager()
    
    mobile_number  = models.IntegerField(unique=True)
    username  = models.CharField(max_length=80, blank=True)
    first_name  = models.CharField(max_length=80, blank=True)
    last_name  = models.CharField(max_length=80, blank=True)
    email  = models.EmailField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    
    USERNAME_FIELD = 'mobile_number'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

