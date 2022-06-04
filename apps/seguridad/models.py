from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User (AbstractBaseUser, PermissionsMixin):
    username = models.CharField("Usuario", max_length=10, unique=True)
    email = models.EmailField("Correo", max_length=100, blank=True)
    first_name = models.CharField("Nombres", max_length=120, blank=True)
    last_name = models.CharField("Apellidos", max_length=120, blank=True)
    birth_date = models.DateField("fecha de Cumpleaño", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username']

    class Meta:
        db_table = 'user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username
