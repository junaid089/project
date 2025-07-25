from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, UserManager
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, role=None, phone_number=None, username=None):
        if not email:
            raise ValueError('Email must be set')
        if not password:
            raise ValueError('Password must be set')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            role=role,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, first_name, last_name, email, password, role, phone_number=None, username=None):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            password = password,
            role = role,
            phone_number = phone_number,
            username =username)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = "admin"
    VENDOR = "vendor"
    USER = "user"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (VENDOR, "Vendor"),
        (USER, "User"),
    ]

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    # is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    license_number = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'role']
    objects = UserManager()

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined', 'username']

    def _str_(self):
        return self.email

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role,"Unknown")

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)