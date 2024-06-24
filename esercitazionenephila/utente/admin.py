from django.contrib import admin
from commento.models import Commento
from risorsa.models import Risorsa
from nodo.models import Nodo
from .models import Utente

admin.site.register(Utente)
admin.site.register(Commento)
admin.site.register(Risorsa)
admin.site.register(Nodo)
