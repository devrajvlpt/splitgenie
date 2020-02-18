# -*- coding: utf-8 -*-
# https://tailwindcss.com/
# python manage.py make migrations your_app_label
# python manage.py migrate --fake-initial your_app_label
from __future__ import unicode_literals
import jwt

from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import now
# accounts.models.py
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class ContactManager(BaseUserManager):

    """Summary
    """

    def normalize_mobile_number(self, mobile_number, country_code=None):
        mobile_number = mobile_number.strip().lower()
        try:
            import phonenumbers
            phone_number = phonenumbers.parse(
                    mobile_number,
                    country_code
            )
            phone = phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164
            )
        except ImportError:
            pass
        return phone

    def create_user(self, user_name, password=None):
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
        if not user_name:
            raise ValueError('Users must have an mobile_number or email address')
        
        if "@" in user_name:
            print("im coming as email")            
            user_name = self.normalize_email(user_name)
            user_name, email, mobile_number = (user_name, user_name, "")
        else:
            print("im coming as mobile_number")
            user_name = self.normalize_mobile_number(user_name, country_code="IN")
            user_name, email, mobile_number = (user_name, "", user_name)

        user = self.model(
            user_name=user_name,
            email=email,
            mobile_number=mobile_number,
            last_login=self.auto_now()
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_splitzuser(self, user_name, password):
        """
        Creates and saves a staff user with the
        given mobile_number and password.
        Args:
            mobile_number (TYPE): Description
            password (TYPE): Description
        Returns:
            TYPE: Description
        """        
        if not user_name:
            raise ValueError('Users must have an mobile_number or email address')
        
        if "@" in user_name:
            user_name = self.normalize_email(user_name)
            user_name, email, mobile_number = (user_name, user_name, "")
        else:
            user_name = self.normalize_mobile_number(user_name, country_code="IN")
            user_name, email, mobile_number = (user_name, "", user_name)

        user = self.model(
            user_name=user_name,
            email=email,
            mobile_number=mobile_number,
            last_login=self.auto_now()
        )
        user.is_active = False
        user.staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        """
        Creates and saves a superuser with
        the given mobile_number and password.
        Args:
            mobile_number (TYPE): Description
            password (TYPE): Description
        Returns:
            TYPE: Description
        """
        if not user_name:
            raise ValueError('Users must have an mobile_number or email address')
        
        if "@" in user_name:
            user_name = self.normalize_email(user_name)
            user_name, email, mobile_number = (user_name, user_name, "")
        else:
            user_name = self.normalize_mobile_number(user_name, country_code="IN")
            user_name, email, mobile_number = (user_name, "", user_name)

        user = self.model(
            user_name=user_name,
            email=email,
            mobile_number=mobile_number,
            last_login=self.auto_now()
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
    user_name = models.CharField(max_length=255, unique=True, default='')
    mobile_number = models.BigIntegerField(blank=True, default=0)
    email = models.EmailField(max_length=254, blank=True, default='')
    first_name = models.CharField(max_length=120, default='')
    last_name = models.CharField(max_length=120, default='')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)    
    registered_time = models.DateTimeField(default=datetime.now())
    USERNAME_FIELD = "user_name"

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        user = {
            'user_name': self.user_name,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        return str(user)

    def has_perm(self, perm, obj=None):
        if self.is_active:
            return True

    def has_module_perms(self, app_label):
        if self.is_active:
            return True
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Friend(models.Model):
    users = models.ManyToManyField(Contact)
    current_user = models.ForeignKey(
        Contact,
        related_name='owner',
        on_delete=models.CASCADE,
        null=True
    )

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        return True

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
        return True


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
    topic_name = models.CharField(
        max_length=240,
        default="splitztopic"
    )
    topic_description = models.CharField(
        max_length=240,
        default="Sharing with Friends and Families"
    )    
    total_amount = models.IntegerField()
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='topic_created',
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='topic_updated',
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
    splitted_user = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                related_name='sa_ledger_user',
                                on_delete=models.CASCADE
                            )
    splitted_amount = models.IntegerField()
    topic_id = models.ForeignKey(
            Topic,
            related_name='sa_ledger_topic',
            on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='sa_ledger_created', 
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name='sa_ledger_updated',
                            on_delete=models.CASCADE
                        )
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
