# -*- coding: utf-8 -*-
# https://tailwindcss.com/
# python manage.py make migrations your_app_label
# python manage.py migrate --fake-initial your_app_label
from __future__ import unicode_literals
import jwt

from django.db import models
from django.contrib.auth.models import User
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
        print ("I'm here for the break")
        user = self.model(
            mobile_number=self.normalize_mobile_number(mobile_number),
            last_login=self.auto_now()
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, mobile_number, password):
        """
        Creates and saves a staff user with the
        given mobile_number and password.
        Args:
            mobile_number (TYPE): Description
            password (TYPE): Description
        Returns:
            TYPE: Description
        """
        user = self.create_user(
            mobile_number,
            password=password,
            last_login=self.auto_now()
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password):
        """
        Creates and saves a superuser with
        the given mobile_number and password.
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
    mobile_number = models.IntegerField(unique=True)
    email = models.EmailField(max_length=254, unique=True, default='')
    first_name = models.CharField(max_length=120, default='')
    last_name = models.CharField(max_length=120, default='')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)    
    registered_time = models.DateTimeField(default=datetime.now())
    USERNAME_FIELD = 'mobile_number'

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        user = {
            'mobile_number':self.mobile_number,
            'first_name':self.first_name,
            'token':self.token
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

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


# Model for Topic members
class TopicMembers(models.Model):
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                related_name='member_list',
                on_delete=models.CASCADE
            )
    current_user = models.ForeignKey(
        Contact,
        related_name='TopicOwner',
        on_delete=models.CASCADE,
        null=True
    )
  

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
    total_amount = models.IntegerField()
    members_list = models.ManyToManyField(TopicMembers, blank=True)
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


# class TopicMembersList(models.Model):
#     member = models.ForeignKey(
#                 TopicMembers,
#                 related_name='member_topic_list',
#                 on_delete=models.CASCADE
#             )
#     topic = models.ForeignKey(
#                 Topic,
#                 related_name='topic_member_list',
#                 on_delete=models.CASCADE
#             )

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
