from django.urls import path
from commento import views


urlpatterns = [
    path('nodi/<int:nodo_id>/risorse/<int:risorsa_id>/commenti', views.post_commento),
]
