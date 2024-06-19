from django.db import models
from utente.models import Utente
from nodo.models import Nodo

# Classe Risorsa fk per owner e nodo di appartenenza
class Risorsa(models.Model):
    owner = models.ForeignKey(
        Utente,
        on_delete=models.CASCADE,
        null=False,
        related_name='risorse'
    )

    nodo  = models.ForeignKey(
        Nodo,
        on_delete=models.CASCADE,
        null=False,
        related_name='risorse'
    )

    responsabile = models.BooleanField(default=False,null=False)
    operatore = models.BooleanField(default=False,null=False)
    titolo = models.CharField(max_length=40,null=False)
    contenuto= models.TextField(null=False)
