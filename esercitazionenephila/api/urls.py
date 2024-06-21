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
    path('nodi/', views_nodi.nodiViews),
    #path('nodi', views_nodi.getNodi,views_nodi.postNodoChild),
]
