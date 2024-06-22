from django.db import models
from utente.models import Utente


#Classe Nodo fk per owner e relazione padre figlio (nullable)
class Nodo(models.Model):
    owner = models.ForeignKey(
        Utente,
        on_delete=models.CASCADE,
        null=False,
        related_name='nodi'
    )
    titolo = models.CharField(max_length=40,null=False, blank=False,default=None)
    padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name='figli'
    )

