from django.urls import path
from utente import views


urlpatterns = [
    # path utenti
    path('register', views.register),
    path('login', views.login),

]
