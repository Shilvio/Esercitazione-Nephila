from django.urls import path
from risorsa import views


urlpatterns = [
    path('nodi/<int:nodo_id>/risorse', views.post_risorsa),
    path('nodi/<int:nodo_id>/risorse/<int:risorsa_id>', views.risorsa_id_handler),
    path('nodi/<int:nodo_id>/risorse/padre', views.post_nuova_risorsa_padre),
]
