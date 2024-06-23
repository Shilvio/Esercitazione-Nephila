from django.urls import path
from utente import views as views_utente
from risorsa import views as views_risorsa
from nodo import views as views_nodo
from commento import views as views_commento

urlpatterns = [
    # path utenti
    path('register/', views_utente.register),
    path('login/', views_utente.login),

    #path nodi
    path('nodo/', views_nodo.post_nodo_root),
    path('nodo/<int:nodo_id>/', views_nodo.nodo_handler),
    path('nodo/<int:nodo_id>/padre/', views_nodo.post_nuovo_child_in_padre),

    #path risorse
    path('nodo/<int:nodo_id>/risorsa/', views_risorsa.post_risorsa),
    path('nodo/<int:nodo_id>/risorsa/<int:risorsa_id>/', views_risorsa.risorsa_id_handler),
    path('nodo/<int:nodo_id>/risorsa/padre', views_risorsa.post_nuova_risorsa_padre),

    #path commenti
    path('nodo/<int:nodo_id>/risorsa/<int:risorsa_id>/commenti', views_commento.post_commento),
]
