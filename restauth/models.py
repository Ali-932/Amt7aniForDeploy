from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone
#abstactbaseuser

class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, email, password,full_name=None,**other_fields):
        if not email:
            raise ValueError('user must have an email to register')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,**other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,fullname=None, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,password,fullname, **other_fields)


    # def create_staffuser(self, email, password, **other_fields):
    #     other_fields['is_staff'] = True
    #     other_fields['is_superuser'] = False
    #     other_fields.setdefault('is_active', True)
    #
    #     return self.save_user(email, password, **other_fields)


class EmailAccount(AbstractBaseUser, PermissionsMixin):
    username = models.NOT_PROVIDED
    email = models.EmailField('Email Address', unique=True)
    full_name = models.CharField(max_length=150, blank=True,null=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmailAccountManager()

    def __str__(self):
        return self.email
