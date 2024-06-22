from django.urls import path
from utente import views as views_utente
from risorsa import views as views_risorsa
from nodo import views as views_nodi
from commento import views as views_commenti

urlpatterns = [
    # path utenti
    path('register/', views_utente.register),
    path('login/', views_utente.login),

    #path nodi
    path('nodo/', views_nodi.postNodoRoot),
    path('nodo/<int:nodo_id>/', views_nodi.nodiChildViews),

    #path risorse
    path('nodo/<int:nodo_id>/risorsa/', views_risorsa.GetRisorsa),
    path('nodo/<int:nodo_id>/risorsa/<int:risorsa_id>', views_risorsa.GetRisorsa)
]
