# -*- coding: utf-8 -*-
# python manage.py make migrations your_app_label
# python manage.py migrate --fake-initial your_app_label

from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.conf import settings
# accounts.models.py

from django.db import models
from django.contrib.auth.models import User

# accounts.models.py

from django.db import models
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
            mobile_number=self.normalize_mobile_number(mobile_number),
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

class Contact(AbstractBaseUser):

    """Summary
    
    Attributes:
        mobile_number (TYPE): Description
        objects (TYPE): Description
    """
    objects = ContactManager()
    mobile_number  = models.IntegerField(unique=True)
    USERNAME_FIELD = 'mobile_number'

class Topic(models.Model):

    """Topic based on share is created
    
    Attributes:
        created_at (TYPE): Description
        created_by (TYPE): Description
        split_number (TYPE): Description
        total_amount (TYPE): Description
        updated_at (TYPE): Description
        updated_by (TYPE): Description
    """
    
    total_amount = models.IntegerField()
    split_number = models.IntegerField()
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name= 'topic_created', 
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name= 'topic_updated',
                            on_delete=models.CASCADE
                        )
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

class SplitAmountLedger(models.Model):

    """List of splitted amount to each user under same topic
    
    Attributes:
        created_at (TYPE): Description
        created_by (TYPE): Description
        splitted_amount (TYPE): Description
        splitted_user (TYPE): Description
        updated_at (TYPE): Description
        updated_by (TYPE): Description
    """
    
    splitted_user  = models.ForeignKey(
                                settings.AUTH_USER_MODEL, 
                                related_name= 'sa_ledger_user', 
                                on_delete=models.CASCADE
                            )
    splitted_amount = models.IntegerField()
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name= 'sa_ledger_created', 
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name= 'sa_ledger_updated',
                            on_delete=models.CASCADE
                        )
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
