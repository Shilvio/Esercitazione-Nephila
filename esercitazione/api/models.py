from django.db import models

# Create your models here.

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

#Classe Nodo fk per owner e relazione padre figlio (nullable)
class Nodo(models.Model):
    owner = models.ForeignKey(
        "Utente",
        on_delete=models.CASCADE,
        null=False,
        related_name='nodi'
    )
    titolo = models.CharField(max_length=40,null=False)
    padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name='figli'
    )

# Classe Risorsa fk per owner e nodo di appartenenza
class Risorsa(models.Model):
    owner = models.ForeignKey(
        "Utente",
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

# Classe Commento fk owner e risorsa
class Commento(models.Model):

    owner = models.ForeignKey(
        Utente,
        on_delete=models.CASCADE,
        null=False,
        related_name='commenti'
    )

    risorsa = models.ForeignKey(
        Risorsa,
        on_delete=models.CASCADE,
        null=False,
        related_name='commenti'
    )

    contenuto = models.TextField(null=False)