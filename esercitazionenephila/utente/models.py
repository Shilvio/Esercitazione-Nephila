from django.db import models

# Classe utente
class Utente(models.Model):

    # ENUM di riuli per le 3 opzioni dalla specifica
    class Ruolo(models.IntegerChoices):
        RESPONSABILE = 0,
        OPERATORE = 1,
        SUPERUTENTE = 2

    username = models.CharField(max_length=40,unique=True,null=False)
    password = models.CharField(max_length=100,null=False)
    ruolo = models.SmallIntegerField(choices= Ruolo,null=False)
    def __str__(self):
        return self.username

