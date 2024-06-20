from django.urls import path
from utente import views as views_utente
from risorsa import views as views_risorsa

urlpatterns = [
    # path utenti
    path('register/', views_utente.register),
    path('login/', views_utente.login),
    #path risorse
    path('testToken/', views_utente.testToken),


]
