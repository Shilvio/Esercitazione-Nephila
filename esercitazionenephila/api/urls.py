from django.urls import path
from utente import views as viewsUtente
from risorsa import views as viewsRisorsa
from nodo import views as viewsNodo
from commento import views as viewsCommento

urlpatterns = [
    # path utenti
    path('register/', viewsUtente.register),
    path('login/', viewsUtente.login),

    #path nodi
    path('nodo/', viewsNodo.postNodoRoot),
    path('nodo/<int:nodo_id>/', viewsNodo.nodoHandler),
    path('nodo/<int:nodo_id>/padre/', viewsNodo.postNuovoChildInPadre),

    #path risorse
    path('nodo/<int:nodo_id>/risorsa/', viewsRisorsa.postRisorsa),
    path('nodo/<int:nodo_id>/risorsa/<int:risorsa_id>/', viewsRisorsa.risorsaIdHandler),
    path('nodo/<int:nodo_id>/risorsa/padre', viewsRisorsa.postNuovaRisorsaPadre),

    #path commenti
    path('nodo/<int:nodo_id>/risorsa/<int:risorsa_id>/commenti', viewsCommento.postCommento),
]
