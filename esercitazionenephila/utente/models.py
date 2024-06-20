from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Classe utente
class Utente(AbstractBaseUser):

    USERNAME_FIELD = 'username'
    # ENUM di riuli per le 3 opzioni dalla specifica
    class Ruolo(models.IntegerChoices):
        RESPONSABILE = 0,
        OPERATORE = 1,
        SUPERUTENTE = 2

    username = models.CharField(max_length=40,unique=True,null=False)
    password = models.CharField(max_length=100,null=False)
    ruolo = models.SmallIntegerField(choices= Ruolo,null=False)
    last_login = models.DateTimeField(("last login"), blank=True, null=True)


