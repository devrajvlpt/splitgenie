from django.db import models
from datetime import datetime, timedelta

from django.conf import settings

import jwt

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
