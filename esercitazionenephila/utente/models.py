from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Classe utente
class CustomUtentiManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('ruolo', 2)
        return self.create_user(username, password, **extra_fields)

class Utente(AbstractBaseUser,PermissionsMixin):

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    # ENUM di riuli per le 3 opzioni dalla specifica
    class Ruolo(models.IntegerChoices):
        RESPONSABILE = 0,
        OPERATORE = 1,
        SUPERUTENTE = 2

    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    username = models.CharField(max_length=40,unique=True,null=False,blank=False)
    password = models.CharField(max_length=100,null=False,blank=False)
    ruolo = models.SmallIntegerField(choices= Ruolo,null=False,blank=False)
    last_login = models.DateTimeField(("last login"), blank=True, null=True)

    objects = CustomUtentiManager()
    REQUIRED_FIELDS = ["password"]
