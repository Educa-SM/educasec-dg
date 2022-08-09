from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, DateField, EmailField
from apps.seguridad.choices import GroupChoices


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
    username = CharField('Usuario', max_length=10, unique=True)
    email = EmailField('Correo', max_length=100, blank=True)
    first_name = CharField('Nombres', max_length=120, blank=True)
    last_name = CharField('Apellidos', max_length=120, blank=True)
    birth_date = DateField('fecha de Cumpleaño', auto_now=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['username']

    class Meta:
        db_table = 'user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.username

    def is_valid_user(self):
        if self.groups.all().exists():
            return True
        return False

    def get_groups(self):
        return self.groups.all()

    def is_user_group(self, id):
        return self.groups.filter(id=id).exists()

    def is_admin_sistema(self):
        return self.is_user_group(GroupChoices.ADMIN_SISTEMA)

    def is_docente(self): #2
        return self.is_user_group(GroupChoices.DOCENTE)

    def is_admin_recursos(self):
        return self.is_user_group(GroupChoices.ADMIN_RECURSOS)

    def is_alumno(self): #4
        return self.is_user_group(GroupChoices.ALUMNO)
