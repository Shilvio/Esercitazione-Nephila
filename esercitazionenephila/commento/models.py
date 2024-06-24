from django.db import models
from utente.models import Utente
from risorsa.models import Risorsa

# Classe Commento fk owner e risorsa
class Commento(models.Model):

    risorsa = models.ForeignKey(
        Risorsa,
        on_delete=models.CASCADE,
        null=False,
        related_name='commenti'
    )

    contenuto = models.TextField(null=False, blank=False,default=None)