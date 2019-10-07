from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from timeslot.models import TimeSlot


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given  email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """ creates a new user by calling _create_user"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ creates a new superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    mode = models.CharField(_('mode'), max_length=10, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(_('sex'), max_length=10, blank=True)
    location = models.CharField(_('location'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user is \
                                    a department staff'))
    is_admin = models.BooleanField(_('admin status'), default=False,
                                   help_text=_('Designates whether the user \
                                    can log into this admin site.')
                                   )
    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_('Designates whether the user \
                                        is a superuser'))
    date_joined = models.DateTimeField(_('date joined'), auto_now=False,
                                       auto_now_add=True)
    date_updated = models.DateTimeField(_('last update'), auto_now=True)
    headline = models.TextField(_('headline'), blank=True)
    about_me = models.TextField(_('about me'), blank=True)
    government_id = models.ImageField(upload_to='government_ids/',
                                      null=True, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15,
                                    blank=True)
    timesheet = models.ManyToManyField(TimeSlot)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
         Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
